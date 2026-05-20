"""
Clause Comparison Service - Sentence-BERT for clause similarity
Identifies similar, alternative, and conflicting clauses
"""

import os
import torch
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple
import numpy as np


class ClauseComparator:
    """Legal clause comparison using fine-tuned Sentence-BERT"""
    
    def __init__(self, checkpoint_path: str = None):
    
        if checkpoint_path is None:
            # Auto-detect fine-tuned model
            base_path = os.path.join(os.path.dirname(__file__), "../../../checkpoints")
            checkpoint_path = os.path.join(base_path, "legal_comparison_model")
            
            if not os.path.exists(checkpoint_path):
                checkpoint_path = "sentence-transformers/all-MiniLM-L6-v2"
        
        self.checkpoint_path = checkpoint_path
        
        print(f"Loading Clause Comparator from: {checkpoint_path}")
        self.model = SentenceTransformer(checkpoint_path)
        print(f"✅ Clause Comparator loaded")
        
        # Similarity thresholds
        self.thresholds = {
            "identical": 0.95,
            "very_similar": 0.85,
            "similar": 0.70,
            "somewhat_similar": 0.50,
            "different": 0.00
        }
    
    def compare_clauses(self, clause1: str, clause2: str) -> Dict:
        # Encode both clauses
        embeddings = self.model.encode([clause1, clause2], convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = torch.nn.functional.cosine_similarity(
            embeddings[0].unsqueeze(0),
            embeddings[1].unsqueeze(0)
        ).item()
        
        # Interpret similarity
        interpretation = self._interpret_similarity(similarity)
        
        return {
            "similarity_score": round(similarity, 3),
            "interpretation": interpretation,
            "clause1_preview": clause1[:100] + "..." if len(clause1) > 100 else clause1,
            "clause2_preview": clause2[:100] + "..." if len(clause2) > 100 else clause2
        }
    
    def find_similar_clauses(self, query_clause: str, candidate_clauses: List[str], 
                            top_k: int = 5, min_similarity: float = 0.5) -> List[Dict]:
        """
        Find most similar clauses to a query clause
        
        Args:
            query_clause: The clause to find matches for
            candidate_clauses: List of clauses to search through
            top_k: Number of top matches to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of top matching clauses with scores
        """
        # Encode query
        query_embedding = self.model.encode(query_clause, convert_to_tensor=True)
        
        # Encode all candidates
        candidate_embeddings = self.model.encode(candidate_clauses, convert_to_tensor=True)
        
        # Calculate similarities
        similarities = torch.nn.functional.cosine_similarity(
            query_embedding.unsqueeze(0),
            candidate_embeddings
        )
        
        # Get top k matches above threshold
        similarities_np = similarities.cpu().numpy()
        top_indices = np.argsort(similarities_np)[::-1]
        
        results = []
        for idx in top_indices[:top_k]:
            score = float(similarities_np[idx])
            if score >= min_similarity:
                results.append({
                    "clause_text": candidate_clauses[idx],
                    "similarity_score": round(score, 3),
                    "interpretation": self._interpret_similarity(score),
                    "clause_preview": candidate_clauses[idx][:100] + "..." 
                                     if len(candidate_clauses[idx]) > 100 
                                     else candidate_clauses[idx]
                })
        
        return results
    
    def compare_documents(self, doc1_clauses: List[str], doc2_clauses: List[str],
                         similarity_threshold: float = 0.7) -> Dict:
        """
        Compare two documents and find matching/differing clauses
        
        Args:
            doc1_clauses: List of clauses from first document
            doc2_clauses: List of clauses from second document
            similarity_threshold: Threshold to consider clauses similar
            
        Returns:
            Dict with matching clauses, unique clauses, and statistics
        """
        matches = []
        doc1_matched = set()
        doc2_matched = set()
        
        # Encode all clauses
        doc1_embeddings = self.model.encode(doc1_clauses, convert_to_tensor=True)
        doc2_embeddings = self.model.encode(doc2_clauses, convert_to_tensor=True)
        
        # Find matches
        for i, emb1 in enumerate(doc1_embeddings):
            similarities = torch.nn.functional.cosine_similarity(
                emb1.unsqueeze(0),
                doc2_embeddings
            )
            
            max_sim_idx = torch.argmax(similarities).item()
            max_sim_score = similarities[max_sim_idx].item()
            
            if max_sim_score >= similarity_threshold:
                matches.append({
                    "doc1_clause": doc1_clauses[i][:100] + "..." if len(doc1_clauses[i]) > 100 else doc1_clauses[i],
                    "doc2_clause": doc2_clauses[max_sim_idx][:100] + "..." if len(doc2_clauses[max_sim_idx]) > 100 else doc2_clauses[max_sim_idx],
                    "similarity_score": round(max_sim_score, 3),
                    "interpretation": self._interpret_similarity(max_sim_score)
                })
                doc1_matched.add(i)
                doc2_matched.add(max_sim_idx)
        
        # Find unique clauses
        doc1_unique = [
            {"clause": doc1_clauses[i][:100] + "..." if len(doc1_clauses[i]) > 100 else doc1_clauses[i]}
            for i in range(len(doc1_clauses)) if i not in doc1_matched
        ]
        
        doc2_unique = [
            {"clause": doc2_clauses[i][:100] + "..." if len(doc2_clauses[i]) > 100 else doc2_clauses[i]}
            for i in range(len(doc2_clauses)) if i not in doc2_matched
        ]
        
        return {
            "num_matches": len(matches),
            "match_percentage": round(len(matches) / max(len(doc1_clauses), len(doc2_clauses)) * 100, 2),
            "matching_clauses": matches,
            "doc1_unique_count": len(doc1_unique),
            "doc1_unique_clauses": doc1_unique[:10],  # Limit to 10 for response size
            "doc2_unique_count": len(doc2_unique),
            "doc2_unique_clauses": doc2_unique[:10],
            "doc1_total_clauses": len(doc1_clauses),
            "doc2_total_clauses": len(doc2_clauses)
        }
    
    def find_alternatives(self, clause: str, clause_bank: List[Dict],
                         min_similarity: float = 0.6, max_similarity: float = 0.9) -> List[Dict]:
        """
        Find alternative formulations of a clause
        
        Args:
            clause: The clause to find alternatives for
            clause_bank: List of candidate clauses with metadata
            min_similarity: Minimum similarity (different but related)
            max_similarity: Maximum similarity (not too identical)
            
        Returns:
            List of alternative clauses
        """
        texts = [c["text"] for c in clause_bank]
        
        # Encode query and candidates
        query_embedding = self.model.encode(clause, convert_to_tensor=True)
        candidate_embeddings = self.model.encode(texts, convert_to_tensor=True)
        
        # Calculate similarities
        similarities = torch.nn.functional.cosine_similarity(
            query_embedding.unsqueeze(0),
            candidate_embeddings
        )
        
        # Filter by similarity range
        alternatives = []
        for i, score in enumerate(similarities):
            score_val = score.item()
            if min_similarity <= score_val <= max_similarity:
                alternatives.append({
                    "clause_text": clause_bank[i]["text"],
                    "clause_type": clause_bank[i].get("type", "Unknown"),
                    "similarity_score": round(score_val, 3),
                    "interpretation": "Alternative formulation",
                    "clause_preview": clause_bank[i]["text"][:100] + "..." 
                                     if len(clause_bank[i]["text"]) > 100 
                                     else clause_bank[i]["text"]
                })
        
        # Sort by similarity
        alternatives.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return alternatives[:10]  # Return top 10
    
    def _interpret_similarity(self, score: float) -> str:
        """Interpret similarity score"""
        if score >= self.thresholds["identical"]:
            return "Identical or near-identical"
        elif score >= self.thresholds["very_similar"]:
            return "Very similar - likely same intent"
        elif score >= self.thresholds["similar"]:
            return "Similar - related content"
        elif score >= self.thresholds["somewhat_similar"]:
            return "Somewhat similar - may be related"
        else:
            return "Different - unrelated content"


# Global instance for API use
_comparator_instance = None

def get_clause_comparator() -> ClauseComparator:
    """Get or create singleton comparator instance"""
    global _comparator_instance
    if _comparator_instance is None:
        _comparator_instance = ClauseComparator()
    return _comparator_instance
