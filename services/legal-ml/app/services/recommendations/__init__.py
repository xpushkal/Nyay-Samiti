"""
Clause Recommendation Service - T5 for clause improvements
Suggests improved or alternative clause formulations
"""

import os
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Dict, List


class ClauseRecommender:
    """Legal clause recommendation using fine-tuned T5"""
    
    def __init__(self, checkpoint_path: str = None):
        """
        Initialize the clause recommender
        
        Args:
            checkpoint_path: Path to fine-tuned model checkpoint
        """
        if checkpoint_path is None:
            # Auto-detect fine-tuned model
            base_path = os.path.join(os.path.dirname(__file__), "../../../checkpoints")
            checkpoint_path = os.path.join(base_path, "t5_recommendations/final")
            
            if not os.path.exists(checkpoint_path):
                checkpoint_path = os.path.join(base_path, "t5_recommendations")
        
        self.checkpoint_path = checkpoint_path
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        print(f"Loading Clause Recommender from: {checkpoint_path}")
        self.tokenizer = T5Tokenizer.from_pretrained(checkpoint_path)
        self.model = T5ForConditionalGeneration.from_pretrained(checkpoint_path)
        self.model.to(self.device)
        self.model.eval()
        print(f"✅ Clause Recommender loaded on {self.device}")
    
    def improve_clause(self, clause: str, num_suggestions: int = 1, max_length: int = 256) -> Dict:
        """
        Generate improved version(s) of a clause
        
        Args:
            clause: Original clause text
            num_suggestions: Number of alternative suggestions to generate
            max_length: Maximum length of generated text
            
        Returns:
            Dict with original clause and suggestions
        """
        # Format input
        input_text = f"improve clause: {clause}"
        
        # Tokenize
        inputs = self.tokenizer(
            input_text,
            max_length=256,
            truncation=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=num_suggestions,
                num_beams=max(4, num_suggestions),
                early_stopping=True,
                temperature=0.8 if num_suggestions > 1 else 1.0,
                do_sample=num_suggestions > 1
            )
        
        # Decode
        suggestions = []
        for output in outputs:
            improved = self.tokenizer.decode(output, skip_special_tokens=True)
            suggestions.append({
                "text": improved,
                "preview": improved[:100] + "..." if len(improved) > 100 else improved
            })
        
        return {
            "original_clause": clause,
            "original_preview": clause[:100] + "..." if len(clause) > 100 else clause,
            "num_suggestions": len(suggestions),
            "suggestions": suggestions
        }
    
    def improve_clauses(self, clauses: List[str], num_suggestions: int = 1) -> List[Dict]:
        """
        Improve multiple clauses
        
        Args:
            clauses: List of clause texts
            num_suggestions: Number of suggestions per clause
            
        Returns:
            List of improvement results
        """
        return [self.improve_clause(clause, num_suggestions) for clause in clauses]
    
    def suggest_alternatives(self, clause: str, num_alternatives: int = 3) -> Dict:
        """
        Generate multiple alternative formulations
        
        Args:
            clause: Original clause
            num_alternatives: Number of alternatives to generate
            
        Returns:
            Dict with original and alternatives
        """
        return self.improve_clause(clause, num_suggestions=num_alternatives)
    
    def batch_improve(self, clauses: List[Dict], suggestion_count: int = 1) -> Dict:
        """
        Improve all clauses in a document
        
        Args:
            clauses: List of clause dicts with 'text' and optionally 'type' keys
            suggestion_count: Number of suggestions per clause
            
        Returns:
            Dict with improvement statistics and results
        """
        results = []
        
        for clause in clauses:
            text = clause.get("text", clause.get("clause_text", ""))
            if not text:
                continue
            
            improvement = self.improve_clause(text, num_suggestions=suggestion_count)
            
            results.append({
                "original_clause": text,
                "clause_type": clause.get("type", clause.get("clause_type", "Unknown")),
                "suggestions": improvement["suggestions"]
            })
        
        return {
            "total_clauses": len(results),
            "suggestions_per_clause": suggestion_count,
            "improvements": results
        }


# Global instance for API use
_recommender_instance = None

def get_clause_recommender() -> ClauseRecommender:
    """Get or create singleton recommender instance"""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = ClauseRecommender()
    return _recommender_instance
