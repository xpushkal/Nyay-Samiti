import json
from pathlib import Path
import random

def create_qa_dataset():
    """Create QA dataset from CUAD"""
    
    print("=" * 80)
    print("CREATING QUESTION ANSWERING DATASET FROM CUAD")
    print("=" * 80)
    print()
    
    cuad_file = Path("datasets/CUAD_full/CUAD_v1.json")
    if not cuad_file.exists():
        print(f"❌ CUAD dataset not found")
        return
    
    print(f"📂 Loading CUAD dataset...")
    with open(cuad_file, 'r') as f:
        cuad_data = json.load(f)
    
    print(f"   ✅ Loaded {len(cuad_data['data'])} documents")
    print()
    
    # Convert to QA format
    qa_examples = []
    
    # Question templates for different clause types
    question_templates = {
        "Termination For Convenience": "What is the termination clause?",
        "Governing Law": "Which law governs this agreement?",
        "Non-Compete": "What are the non-compete restrictions?",
        "Confidentiality": "What are the confidentiality obligations?",
        "Limitation of Liability": "What are the liability limitations?",
        "Audit Rights": "What audit rights are granted?",
        "Insurance": "What insurance requirements are specified?",
        "Expiration Date": "When does this agreement expire?",
        "Notice Period To Terminate Renewal": "What is the notice period for termination?",
        "Anti-Assignment": "Can this agreement be assigned?",
    }
    
    for doc in cuad_data['data']:
        doc_title = doc['title']
        
        for para in doc['paragraphs']:
            context = para['context']
            
            for qa in para['qas']:
                # Skip impossible questions
                if qa.get('is_impossible', False):
                    continue
                
                answers = qa.get('answers', [])
                if not answers:
                    continue
                
                # Extract clause type
                import re
                match = re.search(r'"([^"]+)"', qa['question'])
                if not match:
                    continue
                
                clause_type = match.group(1)
                
                # Get natural question
                natural_question = question_templates.get(
                    clause_type,
                    f"What does the contract say about {clause_type.lower()}?"
                )
                
                # Get first answer
                answer = answers[0]
                answer_text = answer['text'].strip()
                answer_start = answer['answer_start']
                
                if len(answer_text) < 10:  # Skip very short answers
                    continue
                
                qa_examples.append({
                    'id': f"{doc_title}_{len(qa_examples)}",
                    'context': context,
                    'question': natural_question,
                    'answers': {
                        'text': [answer_text],
                        'answer_start': [answer_start]
                    },
                    'clause_type': clause_type,
                    'contract': doc_title
                })
    
    print(f"📊 Dataset Statistics:")
    print(f"   Total QA pairs: {len(qa_examples)}")
    print()
    
    # Sample distribution
    clause_counts = {}
    for ex in qa_examples:
        ctype = ex['clause_type']
        clause_counts[ctype] = clause_counts.get(ctype, 0) + 1
    
    print(f"   Top 10 Question Types:")
    for ctype, count in sorted(clause_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"      {ctype:<35} {count:>4} questions")
    print()
    
    # Save dataset
    output_dir = Path("datasets/qa")
    output_dir.mkdir(exist_ok=True)
    
    # Split into train/dev
    random.shuffle(qa_examples)
    split_point = int(len(qa_examples) * 0.8)
    train_examples = qa_examples[:split_point]
    dev_examples = qa_examples[split_point:]
    
    # Save in SQuAD format
    train_file = output_dir / "train.json"
    with open(train_file, 'w') as f:
        json.dump({
            'version': 'legal_qa_v1',
            'data': [{'paragraphs': train_examples}]
        }, f, indent=2)
    
    dev_file = output_dir / "dev.json"
    with open(dev_file, 'w') as f:
        json.dump({
            'version': 'legal_qa_v1',
            'data': [{'paragraphs': dev_examples}]
        }, f, indent=2)
    
    print(f"✅ Training set saved to: {train_file}")
    print(f"   Size: {len(train_examples)} examples")
    print()
    print(f"✅ Dev set saved to: {dev_file}")
    print(f"   Size: {len(dev_examples)} examples")
    print()
    
    return qa_examples

if __name__ == "__main__":
    examples = create_qa_dataset()
    
    if examples:
        print("=" * 80)
        print("SAMPLE QA PAIRS")
        print("=" * 80)
        print()
        
        for i, ex in enumerate(examples[:3], 1):
            print(f"{i}. Question: {ex['question']}")
            print(f"   Clause Type: {ex['clause_type']}")
            print(f"   Answer: {ex['answers']['text'][0][:150]}...")
            print(f"   Context length: {len(ex['context'])} chars")
            print()
