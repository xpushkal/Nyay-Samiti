from fastapi import APIRouter
from app.models.request_models import TextRequest
from app.services.classification.clause_classifier import ClauseClassifier
router = APIRouter(); clf = ClauseClassifier()
@router.post("/classify")
def classify(req: TextRequest): return {"clauses": clf.predict(req.text)}
