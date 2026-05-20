from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    routes_ner, routes_classification, routes_risk, 
    routes_summary, routes_comparison, routes_recommendations, routes_qa,
    routes_document_analysis,  # New comprehensive analysis routes
    routes_backend_integration,  # Backend integration endpoints
    routes_analysis_trigger  # Analysis trigger for Next.js
)
from app.core.logging_config import setup_logging

app = FastAPI(
    title="Nyay-Samiti Legal AI", 
    version="2.0",
    description="Complete legal document analysis API with 7 AI models"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging()

# Individual ML model endpoints (existing)
app.include_router(routes_ner.router, prefix="/api", tags=["ner"])
app.include_router(routes_classification.router, prefix="/api", tags=["classification"])
app.include_router(routes_risk.router, prefix="/api", tags=["risk"])
app.include_router(routes_summary.router, prefix="/api", tags=["summarization"])
app.include_router(routes_comparison.router, prefix="/api", tags=["comparison"])
app.include_router(routes_recommendations.router, prefix="/api", tags=["recommendations"])
app.include_router(routes_qa.router, prefix="/api", tags=["qa"])

# Complete document analysis endpoints (NEW)
app.include_router(routes_document_analysis.router, prefix="/api", tags=["document-analysis"])

# Backend integration endpoints (for connecting with Next.js)
app.include_router(routes_backend_integration.router, prefix="/api", tags=["backend-integration"])

# Analysis trigger endpoint (Next.js → ML)
app.include_router(routes_analysis_trigger.router, prefix="/api", tags=["analysis-trigger"])

@app.get("/")
def root():
    return {
        "message": "Nyay-Samiti Legal AI API",
        "version": "2.0",
        "docs": "/docs",
        "models": 7,
        "status": "operational"
    }

@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
