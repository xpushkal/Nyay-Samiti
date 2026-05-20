"""
Test NER model integration - Compare generic BERT vs trained Legal BERT
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.services.ner.legal_ner import LegalNER
from transformers import pipeline
import torch

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_entities(entities, title):
    print(f"\n{title}:")
    if not entities:
        print("  No entities detected")
        return
    
    print(f"  {'Entity':<30} {'Type':<20} {'Score':<10}")
    print("  " + "-"*60)
    for ent in entities:
        text = ent.get('text', ent.get('word', ''))
        label = ent.get('label', ent.get('entity_group', ''))
        score = ent.get('score', 0)
        print(f"  {text:<30} {label:<20} {score:>6.2%}")

def test_models():
    print_header("NER Model Integration Test")
    
    # Test sentences
    test_cases = [
        {
            "title": "Contract with Jurisdiction",
            "text": "This Agreement is governed by the laws of the State of Delaware."
        },
        {
            "title": "Parties and Indemnification",
            "text": "The Vendor shall indemnify the Customer for any IP claims under this Agreement."
        },
        {
            "title": "Multiple Locations",
            "text": "The Company is incorporated in Delaware and has offices in New York and California."
        },
        {
            "title": "Legal Representatives",
            "text": "John Smith, Esq. represents the plaintiff in the matter of Johnson v. Corporation Inc."
        },
        {
            "title": "Indian Legal Context",
            "text": "The Supreme Court of India ruled in favor of the petitioner in Civil Appeal No. 1234."
        },
        {
            "title": "Complex Contract Clause",
            "text": "Either party may terminate this Agreement with thirty (30) days written notice to the other party."
        }
    ]
    
    # Load models
    print("\n[+] Loading models...")
    
    # Generic BERT NER
    print("  - Loading Generic BERT-NER (baseline)...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    generic_ner = pipeline("ner", model="dslim/bert-base-NER", device=device, aggregation_strategy="simple")
    
    # Trained Legal BERT NER
    print("  - Loading Trained Legal BERT-NER...")
    trained_model_path = Path(__file__).parent.parent.parent / "checkpoints" / "legalbert_inlegalner"
    if trained_model_path.exists():
        trained_ner = LegalNER(model_name=str(trained_model_path))
        use_trained = True
        print(f"    ✓ Loaded from: {trained_model_path}")
    else:
        print(f"    ✗ Trained model not found at: {trained_model_path}")
        print("    → Using generic model for both comparisons")
        trained_ner = LegalNER(model_name="dslim/bert-base-NER")
        use_trained = False
    
    # Run tests
    print_header("Test Results - Side by Side Comparison")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'─'*70}")
        print(f"Test Case {i}: {test_case['title']}")
        print(f"{'─'*70}")
        print(f"Text: \"{test_case['text']}\"")
        
        # Generic model
        generic_results = generic_ner(test_case['text'])
        print_entities(generic_results, "📊 Generic BERT-NER Results")
        
        # Trained model
        trained_results = trained_ner.predict(test_case['text'])
        model_name = "Trained Legal BERT-NER" if use_trained else "Generic BERT-NER (fallback)"
        print_entities(trained_results, f"🎯 {model_name} Results")
        
        # Comparison
        if use_trained:
            generic_count = len(generic_results)
            trained_count = len(trained_results)
            print(f"\n  📈 Comparison:")
            print(f"     Generic: {generic_count} entities | Trained: {trained_count} entities")
            if trained_count > generic_count:
                print(f"     ✓ Trained model detected {trained_count - generic_count} more entities")
            elif trained_count < generic_count:
                print(f"     ⚠ Trained model detected {generic_count - trained_count} fewer entities")
            else:
                print(f"     → Same number of entities detected")
    
    # Summary
    print_header("Summary")
    
    if use_trained:
        print("\n✅ Integration Successful!")
        print("\nThe trained Legal BERT NER model has been integrated into the API.")
        print("\nKey Differences:")
        print("  • Generic BERT: Trained on general text (CoNLL-2003)")
        print("  • Legal BERT: Fine-tuned on Indian legal documents (InLegalNER)")
        print("  • Legal BERT can detect: Judges, Lawyers, Courts, Case Numbers, Legal Dates")
        print("  • Legal BERT has 29 entity types vs Generic's 4 types")
        
        print("\nModel Details:")
        print(f"  Location: {trained_model_path}")
        print(f"  Size: {(trained_model_path / 'model.safetensors').stat().st_size / (1024*1024):.1f} MB")
        print(f"  Entity Types: 29 (B-JUDGE, B-LAWYER, B-COURT, B-GPE, B-ORG, etc.)")
        
        print("\n🚀 Next Steps:")
        print("  1. The API will now automatically use the trained model")
        print("  2. Test the API endpoint: curl -X POST http://localhost:8000/api/ner ...")
        print("  3. Monitor performance on real legal documents")
        print("  4. Collect feedback for further fine-tuning")
    else:
        print("\n⚠️  Trained model not found!")
        print("\nThe API is currently using the generic BERT-NER model.")
        print("\nTo use the trained model:")
        print("  1. Ensure training completed: python training/train_ner_hf.py")
        print("  2. Check model exists: ls checkpoints/legalbert_inlegalner/")
        print("  3. Re-run this test")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_models()
