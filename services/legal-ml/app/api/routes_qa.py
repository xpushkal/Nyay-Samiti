"""
Question Answering API Routes - Legal document Q&A
"""

from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel
from app.services.qa import get_legal_qa

router = APIRouter()


class AnswerQuestionRequest(BaseModel):
    """Request model for answering a single question"""
    question: str
    context: str
    max_answer_length: int = 100


class MultipleQuestionsRequest(BaseModel):
    """Request model for answering multiple questions"""
    questions: List[str]
    context: str


class ExtractFromDocumentRequest(BaseModel):
    """Request model for extracting information from document"""
    document: str
    questions: List[str]


class AskAboutClausesRequest(BaseModel):
    """Request model for asking about multiple clauses"""
    clauses: List[Dict]  # Each dict should have 'text' and optionally 'type'
    question: str


@router.post("/qa/answer")
def answer_question(req: AnswerQuestionRequest):
    """
    Answer a single question given a context
    
    Returns answer with confidence score
    """
    qa = get_legal_qa()
    result = qa.answer_question(
        req.question,
        req.context,
        req.max_answer_length
    )
    return result


@router.post("/qa/answer_multiple")
def answer_multiple(req: MultipleQuestionsRequest):
    """
    Answer multiple questions about the same context
    
    Returns list of answers
    """
    qa = get_legal_qa()
    results = qa.answer_multiple_questions(
        req.questions,
        req.context
    )
    return {
        "num_questions": len(results),
        "answers": results
    }


@router.post("/qa/extract")
def extract_from_document(req: ExtractFromDocumentRequest):
    """
    Extract information from a full document
    
    Handles long documents by chunking and finding best answers
    """
    qa = get_legal_qa()
    result = qa.extract_from_document(
        req.document,
        req.questions
    )
    return result


@router.post("/qa/ask_clauses")
def ask_about_clauses(req: AskAboutClausesRequest):
    """
    Ask a question about multiple clauses
    
    Expects: List[{"text": str, "type": str}]
    Returns: Best answers from all clauses
    """
    qa = get_legal_qa()
    result = qa.ask_about_clauses(
        req.clauses,
        req.question
    )
    return result
