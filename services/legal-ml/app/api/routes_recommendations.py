"""
Recommendations API Routes - Clause improvement suggestions
"""

from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel
from app.services.recommendations import get_clause_recommender

router = APIRouter()


class ImproveClauseRequest(BaseModel):
    """Request model for improving a single clause"""
    clause: str
    num_suggestions: int = 1
    max_length: int = 256


class ImproveclausesRequest(BaseModel):
    """Request model for improving multiple clauses"""
    clauses: List[str]
    num_suggestions: int = 1


class BatchImproveRequest(BaseModel):
    """Request model for batch improvement"""
    clauses: List[Dict]  # Each dict should have 'text' and optionally 'type'
    suggestion_count: int = 1


@router.post("/recommendations/improve")
def improve_clause(req: ImproveClauseRequest):
    """
    Generate improved version of a clause
    
    Returns original clause and improved suggestions
    """
    recommender = get_clause_recommender()
    result = recommender.improve_clause(
        req.clause,
        req.num_suggestions,
        req.max_length
    )
    return result


@router.post("/recommendations/improve_multiple")
def improve_multiple(req: ImproveclausesRequest):
    """
    Improve multiple clauses
    
    Returns improvements for each clause
    """
    recommender = get_clause_recommender()
    results = recommender.improve_clauses(
        req.clauses,
        req.num_suggestions
    )
    return {
        "total_clauses": len(results),
        "improvements": results
    }


@router.post("/recommendations/alternatives")
def suggest_alternatives(req: ImproveClauseRequest):
    """
    Generate alternative formulations of a clause
    
    Returns multiple different ways to express the same clause
    """
    recommender = get_clause_recommender()
    result = recommender.suggest_alternatives(
        req.clause,
        req.num_suggestions or 3
    )
    return result


@router.post("/recommendations/batch")
def batch_improve(req: BatchImproveRequest):
    """
    Improve all clauses in a document
    
    Expects: List[{"text": str, "type": str}]
    Returns: Improvement suggestions for each clause
    """
    recommender = get_clause_recommender()
    result = recommender.batch_improve(
        req.clauses,
        req.suggestion_count
    )
    return result
