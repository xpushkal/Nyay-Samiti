"""
Comparison API Routes - Clause similarity and document comparison
"""

from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel
from app.services.comparison.clause_comparator import get_clause_comparator

router = APIRouter()


class CompareClausesRequest(BaseModel):
    """Request model for comparing two clauses"""
    clause1: str
    clause2: str


class FindSimilarRequest(BaseModel):
    """Request model for finding similar clauses"""
    query_clause: str
    candidate_clauses: List[str]
    top_k: int = 5
    min_similarity: float = 0.5


class CompareDocumentsRequest(BaseModel):
    """Request model for comparing two documents"""
    doc1_clauses: List[str]
    doc2_clauses: List[str]
    similarity_threshold: float = 0.7


class FindAlternativesRequest(BaseModel):
    """Request model for finding alternative clause formulations"""
    clause: str
    clause_bank: List[Dict]  # Each dict should have 'text' and optionally 'type'
    min_similarity: float = 0.6
    max_similarity: float = 0.9


@router.post("/compare/clauses")
def compare_clauses(req: CompareClausesRequest):
    """
    Compare two clauses for similarity
    
    Returns similarity score (0-1) and interpretation
    """
    comparator = get_clause_comparator()
    result = comparator.compare_clauses(req.clause1, req.clause2)
    return result


@router.post("/compare/find_similar")
def find_similar(req: FindSimilarRequest):
    """
    Find most similar clauses to a query clause
    
    Returns top K matching clauses above minimum similarity threshold
    """
    comparator = get_clause_comparator()
    results = comparator.find_similar_clauses(
        req.query_clause,
        req.candidate_clauses,
        req.top_k,
        req.min_similarity
    )
    return {
        "query_clause": req.query_clause[:100] + "..." if len(req.query_clause) > 100 else req.query_clause,
        "num_results": len(results),
        "similar_clauses": results
    }


@router.post("/compare/documents")
def compare_documents(req: CompareDocumentsRequest):
    """
    Compare two documents to find matching and unique clauses
    
    Returns:
    - Matching clauses between documents
    - Unique clauses in each document
    - Statistics on similarity
    """
    comparator = get_clause_comparator()
    result = comparator.compare_documents(
        req.doc1_clauses,
        req.doc2_clauses,
        req.similarity_threshold
    )
    return result


@router.post("/compare/alternatives")
def find_alternatives(req: FindAlternativesRequest):
    """
    Find alternative formulations of a clause
    
    Returns clauses that are similar but not identical (alternative wordings)
    """
    comparator = get_clause_comparator()
    alternatives = comparator.find_alternatives(
        req.clause,
        req.clause_bank,
        req.min_similarity,
        req.max_similarity
    )
    return {
        "original_clause": req.clause[:100] + "..." if len(req.clause) > 100 else req.clause,
        "num_alternatives": len(alternatives),
        "alternatives": alternatives
    }
