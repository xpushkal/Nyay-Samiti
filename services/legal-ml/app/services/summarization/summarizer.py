from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from pathlib import Path
import re

# Auto-detect trained summarization model
TRAINED_MODEL = Path(__file__).parent.parent.parent.parent / "checkpoints" / "bart_billsum_finetuned" / "final"
DEFAULT_MODEL = "facebook/bart-large-cnn"

class Summarizer:
    def __init__(self, model_name: str = None, device: str = None):
        # Use trained model if available, otherwise fallback to default
        if model_name is None:
            if TRAINED_MODEL.exists():
                model_name = str(TRAINED_MODEL)
                print(f"✅ Using fine-tuned legal summarizer from {model_name}")
            else:
                model_name = DEFAULT_MODEL
                print(f"⚠️  Trained model not found, using generic: {model_name}")
        
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        if device is None: device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.device = device; self.model.to(device)
    
    def _preprocess_legal_text(self, text: str) -> str:
        """Clean and prepare legal text for summarization."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and footers
        text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', text, flags=re.IGNORECASE)
        
        # Remove very short lines (likely formatting artifacts)
        lines = text.split('\n')
        lines = [l.strip() for l in lines if len(l.strip()) > 20]
        text = ' '.join(lines)
        
        return text.strip()
    
    def _post_process_summary(self, summary: str) -> str:
        """Clean up and format the generated summary."""
        # Ensure proper sentence ending
        if summary and not summary[-1] in '.!?':
            summary += '.'
        
        # Remove duplicate sentences
        sentences = [s.strip() + '.' for s in summary.split('.') if s.strip()]
        unique_sentences = []
        seen = set()
        
        for sent in sentences:
            sent_lower = sent.lower()
            if sent_lower not in seen and len(sent.split()) > 3:
                unique_sentences.append(sent)
                seen.add(sent_lower)
        
        return ' '.join(unique_sentences)
        
    def summarize(self, text: str, max_length: int = 180):
        """
        Summarize legal text using fine-tuned BART model.
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length in tokens
            
        Returns:
            Cleaned and formatted summary string
        """
        # Preprocess text
        text = self._preprocess_legal_text(text)
        
        # Use longer input for better context (increased from 3000)
        text = text[:5000]
        
        # Tokenize with proper truncation
        x = self.tok([text], return_tensors="pt", truncation=True, max_length=1024).to(self.device)
        
        # Generate summary with optimized parameters
        with torch.no_grad(): 
            ids = self.model.generate(
                **x, 
                max_new_tokens=max_length,
                min_length=50,  # Ensure minimum length
                num_beams=4,
                length_penalty=2.0,  # Encourage longer summaries
                early_stopping=True,
                no_repeat_ngram_size=3,  # Avoid repetition
                temperature=0.8  # Slight randomness for natural output
            )
        
        summary = self.tok.decode(ids[0], skip_special_tokens=True)
        
        # Post-process for quality
        summary = self._post_process_summary(summary)
        
        return summary