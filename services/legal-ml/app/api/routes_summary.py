from fastapi import APIRouter
from app.models.request_models import TextRequest
from app.services.summarization.summarizer import Summarizer
router = APIRouter(); summ = Summarizer()
@router.post("/summarize")
def summarize(req: TextRequest): return {"summary": summ.summarize(req.text)}
