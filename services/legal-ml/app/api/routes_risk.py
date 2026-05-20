from fastapi import APIRouter
from app.models.request_models import TextRequest
from app.services.risk.risk_scorer import get_risk_scorer
from typing import List, Dict

router = APIRouter()

@router.post("/risk/score", response_model=Dict)
def score_risk(req: TextRequest):
    """
    Score a single clause for risk severity (1-10 scale)
    
    Returns risk score, level, and confidence using fine-tuned Legal BERT
    """
    scorer = get_risk_scorer()
    result = scorer.score_clause(req.text)
    return result

@router.post("/risk/score_document", response_model=Dict)
def score_document_risk(clauses: List[Dict]):
    """
    Score all clauses in a document for risk
    
    Expects: List[{"text": str, "type": str}]
    Returns: Overall risk assessment with clause-level scores
    """
    scorer = get_risk_scorer()
    result = scorer.score_document(clauses)
    return result
