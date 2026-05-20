from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pathlib import Path
import json
import re

# Auto-detect trained CUAD classifier model
TRAINED_MODEL = Path(__file__).parent.parent.parent.parent / "checkpoints" / "legalbert_cuad_classifier" / "checkpoint-1600"
DEFAULT_MODEL = "nlpaueb/legal-bert-base-uncased"

class ClauseClassifier:
    def __init__(self, model_name: str = None, device: str = None):
        # Use trained model if available, otherwise fallback to default
        if model_name is None:
            if TRAINED_MODEL.exists():
                model_name = str(TRAINED_MODEL)
                print(f"✅ Using trained CUAD classifier from {model_name}")
            else:
                model_name = DEFAULT_MODEL
                print(f"⚠️  Trained model not found, using generic: {model_name}")
        
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Load label map if using trained model
        if TRAINED_MODEL.exists() and str(TRAINED_MODEL) in model_name:
            label_map_path = TRAINED_MODEL.parent / "label_map.json"
            if label_map_path.exists():
                with open(label_map_path, 'r') as f:
                    label_data = json.load(f)
                    self.labels = [label_data['id2label'][str(i)] for i in range(len(label_data['id2label']))]
                    print(f"✅ Loaded {len(self.labels)} clause types from trained model")
            else:
                self.labels = [f"Label_{i}" for i in range(self.model.config.num_labels)]
        else:
            # Fallback labels for generic model - comprehensive legal clause types
            self.labels = [
                "Termination", "Indemnification", "Confidentiality", 
                "Limitation of Liability", "Governing Law", "Force Majeure",
                "Payment Terms", "Intellectual Property", "Non-Compete",
                "Dispute Resolution", "Warranties", "Assignment"
            ]
        
        if device is None: device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.device = device; self.model.to(device)
    
    def _split_into_paragraphs(self, text: str):
        """Split text into meaningful paragraphs and clauses."""
        # Split by double newlines first
        paras = text.split("\n\n")
        
        # Further split by numbered clauses (e.g., "1.", "2.", "Article 1")
        all_paras = []
        for p in paras:
            # Split by numbered patterns
            sub_paras = re.split(r'\n(?=\d+\.|\([a-z]\)|\([0-9]+\)|Article\s+\d+|Section\s+\d+)', p)
            all_paras.extend(sub_paras)
        
        # Filter and clean
        cleaned = []
        for p in all_paras:
            p = p.strip()
            # Skip if too short or just a number
            if len(p) < 30 or p.isdigit():
                continue
            # Skip if just a heading (all caps, short)
            if p.isupper() and len(p) < 100:
                continue
            cleaned.append(p)
        
        return cleaned[:20]  # Limit to first 20 clauses for performance
    
    def predict(self, text: str):
        """
        Classify clauses in legal document.
        
        Args:
            text: Document text to classify
            
        Returns:
            List of classified clauses with labels and confidence scores
        """
        paras = self._split_into_paragraphs(text)
        
        if not paras:
            # Fallback: split by sentences if no paragraphs found
            sentences = [s.strip() + '.' for s in text.split('.') if len(s.strip()) > 30]
            paras = sentences[:10]
        
        out = []
        for p in paras:
            # Tokenize and predict
            x = self.tok(p, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            with torch.no_grad(): 
                logits = self.model(**x).logits
            
            probs = torch.softmax(logits, dim=-1)[0].cpu().tolist()
            idx = max(range(len(probs)), key=lambda i: probs[i])
            confidence = probs[idx]
            
            # Only include if confidence is reasonable
            if confidence > 0.1:  # Filter out very low confidence predictions
                out.append({
                    "paragraph": p[:300],  # Increased from 120 for better context
                    "label": self.labels[idx] if idx < len(self.labels) else "General Clause",
                    "score": float(confidence),
                    "full_text": p  # Keep full text for risk assessment
                })
        
        # Sort by confidence
        out.sort(key=lambda x: x["score"], reverse=True)
        return out
