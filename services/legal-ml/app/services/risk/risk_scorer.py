"""
Risk Scoring Service - Fine-tuned Legal BERT for clause risk assessment
Provides 1-10 risk severity scores for legal clauses
"""

import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import Dict, List, Tuple


class RiskScorer:
    """Legal clause risk scoring using fine-tuned Legal BERT"""
    
    def __init__(self, checkpoint_path: str = None):
        """
        Initialize the risk scorer
        
        Args:
            checkpoint_path: Path to fine-tuned model checkpoint
        """
        if checkpoint_path is None:
            # Auto-detect fine-tuned model
            base_path = os.path.join(os.path.dirname(__file__), "../../../checkpoints")
            checkpoint_path = os.path.join(base_path, "legalbert_risk_scorer/final")
            
            if not os.path.exists(checkpoint_path):
                checkpoint_path = os.path.join(base_path, "legalbert_risk_scorer")
        
        self.checkpoint_path = checkpoint_path
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        print(f"Loading Risk Scorer from: {checkpoint_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
        self.model.to(self.device)
        self.model.eval()
        print(f"✅ Risk Scorer loaded on {self.device}")
        
        # Risk level definitions
        self.risk_levels = {
            1: "Minimal",
            2: "Very Low",
            3: "Low",
            4: "Low-Medium",
            5: "Medium",
            6: "Medium-High",
            7: "High",
            8: "Very High",
            9: "Critical",
            10: "Severe"
        }
    
    def score_clause(self, text: str) -> Dict:
        """
        Score a single clause for risk severity
        
        Args:
            text: Clause text to score
            
        Returns:
            Dict with risk_score (1-10), risk_level name, and confidence
        """
        # Tokenize
        inputs = self.tokenizer(
            text,
            max_length=512,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predict
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            
            # Get predicted class and confidence
            probs = torch.softmax(logits, dim=-1)
            risk_score = torch.argmax(probs, dim=-1).item() + 1  # +1 because classes are 0-9
            confidence = probs[0][risk_score - 1].item()
        
        return {
            "risk_score": risk_score,
            "risk_level": self.risk_levels[risk_score],
            "confidence": round(confidence, 3)
        }
    
    def score_clauses(self, texts: List[str]) -> List[Dict]:
        """
        Score multiple clauses in batch
        
        Args:
            texts: List of clause texts
            
        Returns:
            List of risk scoring results
        """
        return [self.score_clause(text) for text in texts]
    
    def score_document(self, clauses: List[Dict]) -> Dict:
        """
        Score all clauses in a document and provide overall risk assessment
        
        Args:
            clauses: List of clause dicts with 'text' and optionally 'type' keys
            
        Returns:
            Dict with overall risk, clause scores, and statistics
        """
        results = []
        total_score = 0
        
        for clause in clauses:
            text = clause.get("text", clause.get("clause_text", ""))
            if not text:
                continue
            
            score_result = self.score_clause(text)
            results.append({
                "clause_text": text[:100] + "..." if len(text) > 100 else text,
                "clause_type": clause.get("type", clause.get("clause_type", "Unknown")),
                **score_result
            })
            total_score += score_result["risk_score"]
        
        # Calculate statistics
        num_clauses = len(results)
        if num_clauses == 0:
            return {
                "overall_risk_score": 0,
                "overall_risk_level": "Unknown",
                "num_clauses": 0,
                "clauses": []
            }
        
        avg_score = total_score / num_clauses
        
        # Categorize clauses by risk
        risk_distribution = {
            "low": len([r for r in results if r["risk_score"] <= 3]),
            "medium": len([r for r in results if 4 <= r["risk_score"] <= 6]),
            "high": len([r for r in results if 7 <= r["risk_score"] <= 8]),
            "critical": len([r for r in results if r["risk_score"] >= 9])
        }
        
        # Get highest risk clauses
        high_risk_clauses = sorted(
            [r for r in results if r["risk_score"] >= 7],
            key=lambda x: x["risk_score"],
            reverse=True
        )[:5]
        
        return {
            "overall_risk_score": round(avg_score, 2),
            "overall_risk_level": self._get_risk_level(avg_score),
            "num_clauses": num_clauses,
            "risk_distribution": risk_distribution,
            "high_risk_clauses": high_risk_clauses,
            "all_clause_scores": results
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level name"""
        if score <= 3:
            return "Low Risk"
        elif score <= 6:
            return "Medium Risk"
        elif score <= 8:
            return "High Risk"
        else:
            return "Critical Risk"


# Global instance for API use
_scorer_instance = None

def get_risk_scorer() -> RiskScorer:
    """Get or create singleton risk scorer instance"""
    global _scorer_instance
    if _scorer_instance is None:
        _scorer_instance = RiskScorer()
    return _scorer_instance
