import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.services.classification.clause_classifier import ClauseClassifier

def test_cuad_classifier():
    """Test the trained CUAD classifier on sample clauses"""
    
    print("=" * 80)
    print("CUAD CLASSIFIER INTEGRATION TEST")
    print("=" * 80)
    print()
    
    # Initialize classifier
    print("📦 Loading CUAD Classifier...")
    classifier = ClauseClassifier()
    print(f"   Device: {classifier.device}")
    print(f"   Number of labels: {len(classifier.labels)}")
    print()
    
    # Test cases with different clause types
    test_cases = [
        {
            "name": "Termination Clause",
            "text": """Termination for Convenience. Either party may terminate this Agreement 
            upon thirty (30) days' prior written notice to the other party without cause."""
        },
        {
            "name": "Non-Compete Clause",
            "text": """Non-Compete Agreement. During the term of this Agreement and for a period 
            of two (2) years thereafter, Employee shall not directly or indirectly engage in any 
            business that competes with the Company's business."""
        },
        {
            "name": "Governing Law",
            "text": """Governing Law. This Agreement shall be governed by and construed in accordance 
            with the laws of the State of California, without regard to its conflict of laws principles."""
        },
        {
            "name": "IP Ownership",
            "text": """Intellectual Property Ownership. All intellectual property rights, including 
            patents, copyrights, and trade secrets, created during the term of this Agreement shall 
            be owned exclusively by the Company."""
        },
        {
            "name": "Audit Rights",
            "text": """Audit Rights. The Company shall have the right, upon reasonable notice and 
            during normal business hours, to audit the Contractor's records related to this Agreement."""
        },
        {
            "name": "Cap on Liability",
            "text": """Limitation of Liability. In no event shall either party's total liability 
            exceed the amount of fees paid under this Agreement in the twelve (12) months preceding 
            the claim."""
        },
        {
            "name": "Anti-Assignment",
            "text": """Assignment Restrictions. This Agreement may not be assigned by either party 
            without the prior written consent of the other party, and any attempted assignment without 
            such consent shall be void."""
        },
        {
            "name": "Multiple Clauses",
            "text": """Termination. Either party may terminate upon 30 days notice.

Governing Law. This Agreement shall be governed by California law.

Non-Compete. Employee shall not compete with Company for 2 years after termination."""
        }
    ]
    
    print("🧪 Testing Sample Clauses:")
    print("=" * 80)
    print()
    
    total_predictions = 0
    high_confidence = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. Test: {test['name']}")
        print(f"   Input: {test['text'][:100]}...")
        print()
        
        results = classifier.predict(test['text'])
        
        for j, result in enumerate(results, 1):
            total_predictions += 1
            if result['score'] > 0.7:
                high_confidence += 1
            
            confidence_emoji = "🟢" if result['score'] > 0.7 else "🟡" if result['score'] > 0.5 else "🔴"
            print(f"   {confidence_emoji} Paragraph {j}:")
            print(f"      Clause Type: {result['label']}")
            print(f"      Confidence: {result['score']:.2%}")
            print(f"      Text: {result['paragraph']}...")
            print()
        
        print("-" * 80)
        print()
    
    # Summary
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"   Total Predictions: {total_predictions}")
    print(f"   High Confidence (>70%): {high_confidence} ({high_confidence/total_predictions*100:.1f}%)")
    print(f"   Model: {classifier.labels[:5]}... ({len(classifier.labels)} total clause types)")
    print()
    print("✅ Integration test complete!")
    print()

if __name__ == "__main__":
    test_cuad_classifier()
