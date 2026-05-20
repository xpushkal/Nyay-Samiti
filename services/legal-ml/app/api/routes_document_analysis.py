"""
Complete Document Analysis API
Processes documents through all 7 AI models and returns comprehensive results
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional
from datetime import datetime
import uuid

from app.models.request_models import DocumentAnalysisRequest, BatchAnalysisRequest
from app.models.response_models import (
    DocumentAnalysisResponse, 
    BatchAnalysisResponse,
    AnalysisStatus
)
from app.services.classification.clause_classifier import ClauseClassifier
from app.services.ner.legal_ner import LegalNER
from app.services.risk.risk_scorer import get_risk_scorer
from app.services.qa import LegalQA
from app.services.summarization.summarizer import Summarizer
from app.services.comparison.clause_comparator import get_clause_comparator
from app.services.recommendations import get_clause_recommender
from app.services.backend_integration import get_backend_integration

router = APIRouter()

# Global model instances (loaded once)
_models = {
    "classifier": None,
    "ner": None,
    "risk": None,
    "qa": None,
    "summarizer": None,
    "comparator": None,
    "recommender": None
}

# In-memory storage for batch jobs (use Redis/DB in production)
_batch_jobs = {}


def get_models():
    """Lazy load all models"""
    if _models["classifier"] is None:
        print("🔄 Loading all models...")
        _models["classifier"] = ClauseClassifier()
        _models["ner"] = LegalNER()
        _models["risk"] = get_risk_scorer()
        _models["qa"] = LegalQA()
        _models["summarizer"] = Summarizer()
        _models["comparator"] = get_clause_comparator()
        _models["recommender"] = get_clause_recommender()
        print("✅ All models loaded")
    return _models


@router.post("/analyze/complete", response_model=DocumentAnalysisResponse)
async def analyze_document_complete(request: DocumentAnalysisRequest):
    """
    Complete document analysis using all 7 AI models
    
    This endpoint processes a legal document through:
    1. Clause Classification (CUAD)
    2. Named Entity Recognition
    3. Risk Scoring
    4. Document Summarization
    5. Question Answering (if questions provided)
    
    Returns comprehensive analysis results for backend storage
    """
    try:
        models = get_models()
        analysis_id = str(uuid.uuid4())
        
        print(f"📄 Analyzing document: {analysis_id}")
        
        # 1. Classify clauses
        print("  🔍 Classifying clauses...")
        classifications = models["classifier"].predict(request.text)
        
        # 2. Extract entities
        print("  🏷️  Extracting entities...")
        entities = models["ner"].predict(request.text)
        
        # 3. Score risk for each classified clause
        print("  ⚠️  Scoring risks...")
        risks = []
        for clause in classifications:
            risk_result = models["risk"].score_clause(clause["paragraph"])
            risks.append({
                "clause_text": clause["paragraph"],
                "clause_type": clause["label"],
                "risk_score": risk_result.get("score", 0),
                "risk_level": risk_result.get("level", "UNKNOWN"),
                "confidence": risk_result.get("confidence", 0)
            })
        
        # 4. Generate summary
        print("  📝 Generating summary...")
        summary_text = models["summarizer"].summarize(
            request.text, 
            max_length=request.summary_length or 150
        )
        
        # 5. Answer questions (if provided)
        qa_results = []
        if request.questions:
            print(f"  ❓ Answering {len(request.questions)} questions...")
            for question in request.questions:
                answer = models["qa"].answer_question(question, request.text)
                qa_results.append({
                    "question": question,
                    "answer": answer.get("answer", ""),
                    "confidence": answer.get("confidence", 0),
                    "start": answer.get("answer_start", 0),
                    "end": answer.get("answer_end", 0)
                })
        
        # 6. Calculate overall document statistics
        total_clauses = len(classifications)
        high_risk_count = sum(1 for r in risks if r["risk_level"] in ["HIGH", "CRITICAL"])
        avg_risk = sum(r["risk_score"] for r in risks) / total_clauses if total_clauses > 0 else 0
        
        # Prepare response
        response = DocumentAnalysisResponse(
            analysis_id=analysis_id,
            document_id=request.document_id,
            timestamp=datetime.utcnow(),
            
            # Classification results
            clauses=classifications,
            clause_count=total_clauses,
            
            # Entity extraction
            entities=entities,
            entity_count=len(entities),
            
            # Risk assessment
            risks=risks,
            high_risk_count=high_risk_count,
            average_risk_score=round(avg_risk, 2),
            
            # Summarization
            summary=summary_text,
            summary_length=len(summary_text),
            
            # Q&A
            qa_results=qa_results,
            
            # Metadata
            processing_time_ms=0,  # Calculate if needed
            model_versions={
                "classifier": "legalbert-cuad-v1",
                "ner": "legalbert-ner-v1",
                "risk": "legalbert-risk-v1",
                "summarizer": "bart-legal-v1",
                "qa": "legalbert-qa-v1"
            }
        )
        
        print(f"✅ Analysis complete: {analysis_id}")
        
        # Send to backend if configured
        backend = get_backend_integration()
        try:
            result = await backend.send_analysis_result(response.dict())
            if result.get("status") == "failed":
                print(f"⚠️  Backend integration warning: {result.get('error')}")
            else:
                print(f"✅ Results sent to backend successfully")
        except Exception as e:
            print(f"⚠️  Backend integration error: {e}")
            # Don't fail the request if backend is down
        
        return response
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze/batch", response_model=BatchAnalysisResponse)
async def analyze_batch(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Batch document analysis (async processing)
    
    Submits multiple documents for processing
    Returns a job ID to check status
    """
    job_id = str(uuid.uuid4())
    
    # Store job info
    _batch_jobs[job_id] = {
        "status": "queued",
        "total_documents": len(request.documents),
        "processed": 0,
        "results": [],
        "started_at": datetime.utcnow(),
        "completed_at": None
    }
    
    # Process in background
    background_tasks.add_task(process_batch, job_id, request.documents)
    
    return BatchAnalysisResponse(
        job_id=job_id,
        status="queued",
        total_documents=len(request.documents),
        message=f"Batch job {job_id} queued for processing"
    )


@router.get("/analyze/batch/{job_id}", response_model=BatchAnalysisResponse)
async def get_batch_status(job_id: str):
    """Get status of batch analysis job"""
    if job_id not in _batch_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = _batch_jobs[job_id]
    
    return BatchAnalysisResponse(
        job_id=job_id,
        status=job["status"],
        total_documents=job["total_documents"],
        processed=job["processed"],
        results=job["results"],
        started_at=job["started_at"],
        completed_at=job["completed_at"]
    )


async def process_batch(job_id: str, documents: List[Dict]):
    """Background task to process batch of documents"""
    try:
        _batch_jobs[job_id]["status"] = "processing"
        models = get_models()
        
        for idx, doc in enumerate(documents):
            try:
                # Process each document
                request = DocumentAnalysisRequest(**doc)
                result = await analyze_document_complete(request)
                
                _batch_jobs[job_id]["results"].append({
                    "document_id": doc.get("document_id"),
                    "status": "success",
                    "result": result.dict()
                })
                
            except Exception as e:
                _batch_jobs[job_id]["results"].append({
                    "document_id": doc.get("document_id"),
                    "status": "failed",
                    "error": str(e)
                })
            
            _batch_jobs[job_id]["processed"] = idx + 1
        
        _batch_jobs[job_id]["status"] = "completed"
        _batch_jobs[job_id]["completed_at"] = datetime.utcnow()
        
    except Exception as e:
        _batch_jobs[job_id]["status"] = "failed"
        _batch_jobs[job_id]["error"] = str(e)


@router.post("/analyze/clauses/compare")
async def compare_clauses_batch(clauses: List[str]):
    """
    Compare multiple clauses for similarity
    Returns similarity matrix
    """
    try:
        models = get_models()
        comparator = models["comparator"]
        
        n = len(clauses)
        similarity_matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    similarity_matrix[i][j] = 1.0
                else:
                    result = comparator.compare_clauses(clauses[i], clauses[j])
                    score = result.get("similarity_score", 0)
                    similarity_matrix[i][j] = score
                    similarity_matrix[j][i] = score
        
        return {
            "clause_count": n,
            "similarity_matrix": similarity_matrix,
            "clauses": clauses
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/clauses/improve")
async def improve_clauses_batch(clauses: List[Dict]):
    """
    Batch clause improvement recommendations
    
    Input: [{"text": "clause text", "type": "clause type"}]
    Output: Improved versions of all clauses
    """
    try:
        models = get_models()
        recommender = models["recommender"]
        
        improvements = []
        
        for clause in clauses:
            result = recommender.improve_clause(
                clause["text"],
                num_suggestions=clause.get("num_suggestions", 1)
            )
            
            improvements.append({
                "original": clause["text"],
                "type": clause.get("type", "Unknown"),
                "suggestions": result["suggestions"]
            })
        
        return {
            "total_clauses": len(clauses),
            "improvements": improvements
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/export")
async def export_analysis(analysis_id: str, format: str = "json"):
    """
    Export analysis results in various formats
    
    Supported formats: json, csv, pdf
    """
    # TODO: Implement export functionality
    # This would integrate with your backend to fetch stored results
    
    return {
        "message": "Export functionality - integrate with your backend",
        "analysis_id": analysis_id,
        "format": format
    }
