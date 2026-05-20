"""
Document Analysis Trigger Endpoint
Endpoint for Next.js to trigger ML analysis
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
import asyncio

from app.services.classification.clause_classifier import ClauseClassifier
from app.services.ner.legal_ner import LegalNER
from app.services.risk.risk_scorer import get_risk_scorer
from app.services.summarization.summarizer import Summarizer
from app.services.backend_integration import get_backend_integration

logger = logging.getLogger(__name__)

router = APIRouter()

# Global model instances
_models = None


class AnalyzeDocumentRequest(BaseModel):
    analysis_id: Optional[str] = None
    document_id: str
    document_text: str
    analysis_type: str = "comprehensive"


class AnalyzeDocumentResponse(BaseModel):
    analysis_id: str
    status: str
    message: str


def get_models():
    """Load all ML models"""
    global _models
    if _models is None:
        logger.info("🔄 Loading ML models...")
        _models = {
            "classifier": ClauseClassifier(),
            "ner": LegalNER(),
            "risk": get_risk_scorer(),
            "summarizer": Summarizer(),
        }
        logger.info("✅ ML models loaded")
    return _models


async def process_document_analysis(document_id: str, document_text: str, analysis_id: str):
    """Background task to process document analysis"""
    try:
        backend = get_backend_integration()
        
        # Update status to processing
        await backend.update_analysis_status(analysis_id, "processing", 10)
        
        models = get_models()
        
        # 1. Extract entities (25%)
        logger.info(f"📊 Extracting entities for {analysis_id}")
        entities = models["ner"].predict(document_text)
        await backend.update_analysis_status(analysis_id, "processing", 25)
        
        # 2. Classify clauses (50%)
        logger.info(f"🔍 Classifying clauses for {analysis_id}")
        classifications = models["classifier"].predict(document_text)
        await backend.update_analysis_status(analysis_id, "processing", 50)
        
        # 3. Risk assessment (75%)
        logger.info(f"⚠️  Assessing risks for {analysis_id}")
        risk_scores = []
        for clause in classifications[:5]:  # Top 5 clauses
            try:
                risk = models["risk"].score_clause(clause["paragraph"])
                logger.info(f"Risk result: {risk}")
                risk_scores.append({
                    "clause": clause["paragraph"][:200],
                    "type": clause["label"],
                    "risk_score": risk.get("risk_score", 0),
                    "risk_level": risk.get("risk_level", "UNKNOWN"),
                    "confidence": risk.get("confidence", 0),
                })
            except Exception as e:
                logger.error(f"Failed to score clause: {e}")
                risk_scores.append({
                    "clause": clause["paragraph"][:200],
                    "type": clause["label"],
                    "risk_score": 0,
                    "risk_level": "ERROR",
                    "confidence": 0,
                })
        
        overall_risk = sum(r["risk_score"] for r in risk_scores) / len(risk_scores) if risk_scores else 0
        await backend.update_analysis_status(analysis_id, "processing", 75)
        
        # 4. Summarization (90%)
        logger.info(f"📝 Generating summary for {analysis_id}")
        summary = models["summarizer"].summarize(
            document_text,
            max_length=200  # Increased for better summaries
        )
        await backend.update_analysis_status(analysis_id, "processing", 90)
        
        # Prepare results with improved structure
        results = {
            "entities": entities,
            "classification": {
                "document_type": classifications[0]["label"] if classifications else "Unknown",
                "confidence": classifications[0]["score"] if classifications else 0,
                "clauses": classifications[:15],  # Increased from 10 to 15 clauses
            },
            "risk_assessment": {
                "risk_score": overall_risk,
                "risk_level": "high" if overall_risk > 0.7 else "medium" if overall_risk > 0.4 else "low",
                "risk_factors": risk_scores,
            },
            "summary": summary,
            "qa_results": [],
        }
        
        # Log summary of results for debugging
        logger.info(f"📊 Analysis Results Summary for {analysis_id}:")
        logger.info(f"  - Entities: {len(entities)}")
        logger.info(f"  - Clauses: {len(classifications)}")
        logger.info(f"  - Risk Factors: {len(risk_scores)}")
        logger.info(f"  - Summary Length: {len(summary.split())} words")
        
        # Send results to backend
        logger.info(f"✅ Sending results for {analysis_id}")
        await backend.send_analysis_result({
            "analysis_id": analysis_id,
            "document_id": document_id,
            "status": "completed",
            "results": results,
            "timestamp": "2025-10-26T10:00:00Z",
            "analysis_type": "comprehensive",
        })
        
        logger.info(f"🎉 Analysis complete: {analysis_id}")
        
    except Exception as e:
        logger.error(f"❌ Analysis failed for {analysis_id}: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        backend = get_backend_integration()
        await backend.send_analysis_result({
            "analysis_id": analysis_id,
            "document_id": document_id,
            "status": "failed",
            "error": str(e),
            "timestamp": "2025-10-26T10:00:00Z",
            "analysis_type": "comprehensive",
        })


@router.post("/document/analyze", response_model=AnalyzeDocumentResponse)
async def analyze_document(
    request: AnalyzeDocumentRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger ML analysis for a document
    
    This endpoint is called by Next.js backend to start analysis.
    Processing happens in background and results are sent back via callback.
    
    **Flow:**
    1. Next.js calls this endpoint with document data
    2. Analysis starts in background
    3. Progress updates sent to Next.js via /api/analysis/{id}/status
    4. Final results sent to Next.js via /api/analysis/results
    """
    try:
        # Use provided analysis_id or generate one
        if request.analysis_id:
            analysis_id = request.analysis_id
        else:
            analysis_id = f"analysis_{request.document_id}_{hash(request.document_text[:100]) % 10000}"
        
        logger.info(f"🚀 Starting analysis: {analysis_id}")
        
        # Start background processing
        background_tasks.add_task(
            process_document_analysis,
            request.document_id,
            request.document_text,
            analysis_id
        )
        
        return AnalyzeDocumentResponse(
            analysis_id=analysis_id,
            status="queued",
            message="Analysis started successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/document/analyze/{analysis_id}/status")
async def get_analysis_status(analysis_id: str):
    """
    Get analysis status (proxied from Next.js backend)
    """
    try:
        backend = get_backend_integration()
        # In real implementation, you'd fetch from Next.js backend
        return {
            "analysis_id": analysis_id,
            "status": "processing",
            "progress": 50,
            "message": "Analysis in progress"
        }
    except Exception as e:
        logger.error(f"❌ Failed to get status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
