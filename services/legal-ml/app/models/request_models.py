from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TextRequest(BaseModel): 
    text: str

class DocumentAnalysisRequest(BaseModel):
    """Request for complete document analysis"""
    text: str = Field(..., description="Legal document text to analyze")
    document_id: Optional[str] = Field(None, description="Optional document identifier")
    questions: Optional[List[str]] = Field(None, description="Questions to answer about the document")
    summary_length: Optional[int] = Field(150, description="Maximum summary length")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class BatchAnalysisRequest(BaseModel):
    """Request for batch document analysis"""
    documents: List[Dict[str, Any]] = Field(..., description="List of documents to analyze")
    callback_url: Optional[str] = Field(None, description="URL to notify when batch is complete")
class SearchRequest(BaseModel):
    query: str
    k: int = 5
