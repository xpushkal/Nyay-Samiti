from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from pathlib import Path
import re

# Use trained legal NER model if available, otherwise fall back to generic BERT
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TRAINED_MODEL = BASE_DIR / "checkpoints" / "legalbert_inlegalner"
DEFAULT_MODEL = str(TRAINED_MODEL) if TRAINED_MODEL.exists() else "dslim/bert-base-NER"

class LegalNER:
    def __init__(self, model_name: str = DEFAULT_MODEL, device: str = None):
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        if device is None: device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.device = device; self.model.to(device)
        
        # Mapping for user-friendly entity type names
        self.type_mapping = {
            "PER": "PERSON",
            "PERSON": "PERSON",
            "ORG": "ORGANIZATION",
            "ORGANIZATION": "ORGANIZATION",
            "LOC": "LOCATION",
            "LOCATION": "LOCATION",
            "GPE": "LOCATION",
            "DATE": "DATE",
            "TIME": "TIME",
            "MONEY": "MONEY",
            "PERCENT": "PERCENT",
            "QUANTITY": "QUANTITY",
            "CARDINAL": "NUMBER",
            "ORDINAL": "NUMBER",
            "LAW": "LAW",
            "PRODUCT": "PRODUCT",
            "EVENT": "EVENT",
            "WORK_OF_ART": "DOCUMENT",
            "LANGUAGE": "LANGUAGE",
            "NORP": "GROUP",
            "FAC": "FACILITY"
        }
    
    def _clean_entity_text(self, text: str) -> str:
        """Clean up entity text by removing extra whitespace and punctuation."""
        # Remove leading/trailing whitespace and punctuation
        text = text.strip()
        text = re.sub(r'^[^\w]+|[^\w]+$', '', text)
        return text
    
    def _is_valid_entity(self, text: str, entity_type: str) -> bool:
        """Check if entity is valid and meaningful."""
        text = text.strip()
        
        # Must have at least 2 characters
        if len(text) < 2:
            return False
        
        # Must contain at least one letter
        if not re.search(r'[a-zA-Z]', text):
            return False
        
        # Filter out common stopwords and meaningless tokens
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        if text.lower() in stopwords:
            return False
        
        # Filter out standalone numbers unless it's a DATE or MONEY
        if entity_type not in ["DATE", "TIME", "MONEY", "PERCENT", "NUMBER"] and text.isdigit():
            return False
        
        return True
    
    def _get_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Extract context around an entity."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        context = text[context_start:context_end].strip()
        
        # Add ellipsis if truncated
        if context_start > 0:
            context = "..." + context
        if context_end < len(text):
            context += "..."
        
        return context
    
    def _merge_subword_entities(self, entities: list, text: str) -> list:
        """Merge subword entities (e.g., 'John' and '##son' -> 'Johnson')."""
        if not entities:
            return []
        
        merged = []
        current = None
        
        for entity in entities:
            entity_text = entity["text"]
            entity_label = entity["label"]
            
            # Remove B- and I- prefixes
            if entity_label.startswith("B-") or entity_label.startswith("I-"):
                base_label = entity_label[2:]
            else:
                base_label = entity_label
            
            # If this is a continuation (I-) and same type as current, merge
            if current and entity_label.startswith("I-") and base_label == current["base_label"]:
                current["end"] = entity["end"]
                current["text"] = text[current["start"]:current["end"]]
                current["score"] = max(current["score"], entity["score"])
            else:
                # Save previous entity
                if current:
                    merged.append(current)
                
                # Start new entity
                current = {
                    "text": entity_text,
                    "type": base_label,
                    "base_label": base_label,
                    "start": entity["start"],
                    "end": entity["end"],
                    "score": entity["score"]
                }
        
        # Add last entity
        if current:
            merged.append(current)
        
        return merged
    
    def predict(self, text: str):
        # Process in chunks to handle long documents
        max_length = 512
        entities_raw = []
        
        # Split text into chunks
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) > max_length * 3:  # Rough estimate
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        # Process each chunk
        offset = 0
        for chunk in chunks[:3]:  # Limit to first 3 chunks for performance
            x = self.tok(chunk, return_offsets_mapping=True, return_tensors="pt", truncation=True, max_length=max_length).to(self.device)
            with torch.no_grad():
                logits = self.model(**{k:v for k,v in x.items() if k!='offset_mapping'}).logits
                probs = torch.softmax(logits, dim=-1)
                labels = probs.argmax(dim=-1).cpu().numpy()[0]
                scores = probs.max(dim=-1).values.cpu().numpy()[0]
            
            offsets = x['offset_mapping'][0].tolist()
            id2label = self.model.config.id2label
            
            for i, lab in enumerate(labels):
                label_name = id2label.get(lab, "O")
                # Skip O (non-entity) labels and special tokens
                if lab == 0 or label_name == "O" or label_name.startswith("["):
                    continue
                s, e = offsets[i]
                if e > s:
                    entities_raw.append({
                        "label": label_name,
                        "start": int(s) + offset,
                        "end": int(e) + offset,
                        "text": chunk[s:e],
                        "score": float(scores[i])
                    })
            
            offset += len(chunk) + 1
        
        # Merge subword entities
        merged_entities = self._merge_subword_entities(entities_raw, text)
        
        # Clean and filter entities
        out = []
        seen_texts = set()
        
        for entity in merged_entities:
            # Map entity type to user-friendly name
            entity_type = entity["type"]
            for key, value in self.type_mapping.items():
                if key in entity_type.upper():
                    entity_type = value
                    break
            
            # Clean entity text
            entity_text = self._clean_entity_text(entity["text"])
            
            # Validate entity
            if not self._is_valid_entity(entity_text, entity_type):
                continue
            
            # Remove duplicates
            if entity_text.lower() in seen_texts:
                continue
            seen_texts.add(entity_text.lower())
            
            # Get context
            context = self._get_context(text, entity["start"], entity["end"])
            
            out.append({
                "text": entity_text,
                "type": entity_type,
                "score": entity["score"],
                "context": context
            })
        
        # Sort by score and return top entities
        out.sort(key=lambda x: x["score"], reverse=True)
        return out[:50]  # Limit to top 50 entities
