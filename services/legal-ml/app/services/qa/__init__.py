"""
Question Answering Service - Legal BERT for extractive QA
Answers questions about legal documents
"""

import os
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from typing import Dict, List


class LegalQA:
    """Legal question answering using fine-tuned Legal BERT"""
    
    def __init__(self, checkpoint_path: str = None):
        """
        Initialize the QA system
        
        Args:
            checkpoint_path: Path to fine-tuned model checkpoint
        """
        if checkpoint_path is None:
            # Auto-detect fine-tuned model
            base_path = os.path.join(os.path.dirname(__file__), "../../../checkpoints")
            checkpoint_path = os.path.join(base_path, "legalbert_qa/final")
            
            if not os.path.exists(checkpoint_path):
                checkpoint_path = os.path.join(base_path, "legalbert_qa")
        
        self.checkpoint_path = checkpoint_path
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        print(f"Loading Legal QA from: {checkpoint_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(checkpoint_path)
        self.model.to(self.device)
        self.model.eval()
        print(f"✅ Legal QA loaded on {self.device}")
    
    def answer_question(self, question: str, context: str, max_answer_length: int = 100) -> Dict:
        """
        Answer a question given a context
        
        Args:
            question: The question to answer
            context: The context containing the answer
            max_answer_length: Maximum length of answer
            
        Returns:
            Dict with answer, confidence, and position
        """
        # Tokenize
        inputs = self.tokenizer(
            question,
            context,
            max_length=384,
            truncation="only_second",
            padding="max_length",
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predict
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Get start and end positions
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        
        # Get best start and end positions
        start_idx = torch.argmax(start_logits).item()
        end_idx = torch.argmax(end_logits).item()
        
        # Ensure end >= start and within max length
        if end_idx < start_idx:
            end_idx = start_idx
        if end_idx - start_idx > max_answer_length:
            end_idx = start_idx + max_answer_length
        
        # Get confidence scores
        start_confidence = torch.softmax(start_logits, dim=-1)[0][start_idx].item()
        end_confidence = torch.softmax(end_logits, dim=-1)[0][end_idx].item()
        confidence = (start_confidence + end_confidence) / 2
        
        # Extract answer
        answer_tokens = inputs["input_ids"][0][start_idx:end_idx+1]
        answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
        
        # If answer is empty or just the question, indicate no answer found
        if not answer or answer.lower() == question.lower():
            answer = "[No clear answer found in context]"
            confidence = 0.0
        
        return {
            "question": question,
            "answer": answer,
            "confidence": round(confidence, 3),
            "context_preview": context[:150] + "..." if len(context) > 150 else context,
            "answer_start": start_idx,
            "answer_end": end_idx
        }
    
    def answer_multiple_questions(self, questions: List[str], context: str) -> List[Dict]:
        """
        Answer multiple questions about the same context
        
        Args:
            questions: List of questions
            context: The context containing answers
            
        Returns:
            List of answer dicts
        """
        return [self.answer_question(q, context) for q in questions]
    
    def extract_from_document(self, document: str, questions: List[str]) -> Dict:
        """
        Extract information from a document using questions
        
        Args:
            document: Full document text
            questions: List of questions to answer
            
        Returns:
            Dict with extracted information
        """
        # Split document into chunks if too long
        max_context_length = 2000  # characters
        
        if len(document) <= max_context_length:
            contexts = [document]
        else:
            # Simple chunking by sentences
            sentences = document.split('. ')
            contexts = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < max_context_length:
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        contexts.append(current_chunk)
                    current_chunk = sentence + ". "
            
            if current_chunk:
                contexts.append(current_chunk)
        
        # Answer each question, trying all contexts
        results = []
        
        for question in questions:
            best_answer = None
            best_confidence = 0.0
            
            for context in contexts:
                answer = self.answer_question(question, context)
                
                if answer["confidence"] > best_confidence:
                    best_confidence = answer["confidence"]
                    best_answer = answer
            
            if best_answer:
                results.append(best_answer)
        
        return {
            "document_length": len(document),
            "num_chunks": len(contexts),
            "num_questions": len(questions),
            "answers": results
        }
    
    def ask_about_clauses(self, clauses: List[Dict], question: str) -> Dict:
        """
        Ask a question about multiple clauses
        
        Args:
            clauses: List of clause dicts with 'text' key
            question: Question to ask
            
        Returns:
            Dict with answers from each clause
        """
        results = []
        
        for i, clause in enumerate(clauses):
            text = clause.get("text", clause.get("clause_text", ""))
            if not text:
                continue
            
            answer = self.answer_question(question, text)
            answer["clause_index"] = i
            answer["clause_type"] = clause.get("type", clause.get("clause_type", "Unknown"))
            
            # Only include if confidence is reasonable
            if answer["confidence"] > 0.1:
                results.append(answer)
        
        # Sort by confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "question": question,
            "total_clauses": len(clauses),
            "answers_found": len(results),
            "best_answers": results[:5]  # Top 5 answers
        }


# Global instance for API use
_qa_instance = None

def get_legal_qa() -> LegalQA:
    """Get or create singleton QA instance"""
    global _qa_instance
    if _qa_instance is None:
        _qa_instance = LegalQA()
    return _qa_instance
