from fastapi import APIRouter
from app.models.request_models import TextRequest
from app.services.ner.legal_ner import LegalNER
router = APIRouter(); ner = LegalNER()
@router.post("/ner")
def do_ner(req: TextRequest): return {"entities": ner.predict(req.text)}
