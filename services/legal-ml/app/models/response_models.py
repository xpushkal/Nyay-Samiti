from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class Entity(BaseModel): 
    label: str
    start: int
    end: int
    text: str
    score: float

class Clause(BaseModel): 
    type: str
    start: int
    end: int
    score: float

class RiskItem(BaseModel): 
    clause_type: str
    rule: str
    severity: str
    explanation: str
    start: int
    end: int

class AnalysisResponse(BaseModel):
    entities: List[Entity] = []
    clauses: List[Clause] = []
    risks: List[RiskItem] = []
    summary: str = ""
    retrieval: List[Dict[str, Any]] = []


class AnalysisStatus(str, Enum):
    """Status of document analysis"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentAnalysisResponse(BaseModel):
    """Complete document analysis response"""
    # Identification
    analysis_id: str = Field(..., description="Unique analysis identifier")
    document_id: Optional[str] = Field(None, description="Document identifier")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    
    # Classification results
    clauses: List[Dict[str, Any]] = Field(default_factory=list, description="Classified clauses")
    clause_count: int = Field(0, description="Total number of clauses")
    
    # Entity extraction
    entities: List[Dict[str, Any]] = Field(default_factory=list, description="Extracted entities")
    entity_count: int = Field(0, description="Total number of entities")
    
    # Risk assessment
    risks: List[Dict[str, Any]] = Field(default_factory=list, description="Risk assessments")
    high_risk_count: int = Field(0, description="Number of high-risk clauses")
    average_risk_score: float = Field(0.0, description="Average risk score")
    
    # Summarization
    summary: str = Field("", description="Document summary")
    summary_length: int = Field(0, description="Summary character count")
    
    # Q&A
    qa_results: List[Dict[str, Any]] = Field(default_factory=list, description="Question answers")
    
    # Metadata
    processing_time_ms: int = Field(0, description="Processing time in milliseconds")
    model_versions: Dict[str, str] = Field(default_factory=dict, description="Model versions used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "123e4567-e89b-12d3-a456-426614174000",
                "document_id": "contract_001",
                "timestamp": "2025-10-26T12:00:00Z",
                "clause_count": 10,
                "entity_count": 15,
                "high_risk_count": 2,
                "average_risk_score": 5.5
            }
        }


class BatchAnalysisResponse(BaseModel):
    """Batch analysis response"""
    job_id: str = Field(..., description="Batch job identifier")
    status: str = Field(..., description="Job status (queued/processing/completed/failed)")
    total_documents: int = Field(..., description="Total documents in batch")
    processed: int = Field(0, description="Number of processed documents")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Analysis results")
    message: Optional[str] = Field(None, description="Status message")
    started_at: Optional[datetime] = Field(None, description="Job start time")
    completed_at: Optional[datetime] = Field(None, description="Job completion time")
