import json
from pathlib import Path
from collections import defaultdict
import random

def create_comparison_dataset():
    """Create contract comparison dataset from CUAD"""
    
    print("=" * 80)
    print("CREATING CONTRACT COMPARISON DATASET")
    print("=" * 80)
    print()
    
    cuad_file = Path("datasets/CUAD_full/CUAD_v1.json")
    if not cuad_file.exists():
        print(f"❌ CUAD dataset not found at {cuad_file}")
        return
    
    print(f"📂 Loading CUAD dataset...")
    with open(cuad_file, 'r') as f:
        cuad_data = json.load(f)
    
    print(f"   ✅ Loaded {len(cuad_data['data'])} documents")
    print()
    
    # Group clauses by type
    clause_groups = defaultdict(list)
    
    for doc in cuad_data['data']:
        doc_title = doc['title']
        for para in doc['paragraphs']:
            context = para['context']
            
            for qa in para['qas']:
                question = qa['question']
                
                # Extract clause type
                import re
                match = re.search(r'"([^"]+)"', question)
                if not match:
                    continue
                    
                clause_type = match.group(1)
                
                # Get answers
                has_clause = qa.get('is_impossible', False) == False and len(qa.get('answers', [])) > 0
                
                if has_clause:
                    for answer in qa['answers']:
                        answer_text = answer['text'].strip()
                        if answer_text and len(answer_text) > 30:
                            clause_groups[clause_type].append({
                                'text': answer_text,
                                'contract': doc_title,
                                'clause_type': clause_type
                            })
    
    print(f"📊 Clause Groups:")
    print(f"   Total clause types: {len(clause_groups)}")
    for ctype, clauses in sorted(clause_groups.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"      {ctype:<35} {len(clauses):>4} clauses")
    print()
    
    # Create comparison pairs
    # 1. Similar pairs (same clause type, different contracts)
    # 2. Dissimilar pairs (different clause types)
    
    similar_pairs = []
    dissimilar_pairs = []
    
    print(f"🔄 Creating comparison pairs...")
    
    # Similar pairs
    for clause_type, clauses in clause_groups.items():
        if len(clauses) < 2:
            continue
        
        # Sample pairs from same clause type
        for i in range(min(50, len(clauses))):
            for j in range(i+1, min(i+3, len(clauses))):
                if clauses[i]['contract'] != clauses[j]['contract']:
                    similar_pairs.append({
                        'text1': clauses[i]['text'],
                        'text2': clauses[j]['text'],
                        'contract1': clauses[i]['contract'],
                        'contract2': clauses[j]['contract'],
                        'clause_type': clause_type,
                        'label': 1,  # Similar
                        'similarity': 0.8 + random.random() * 0.2  # 0.8-1.0
                    })
    
    # Dissimilar pairs
    clause_types = list(clause_groups.keys())
    for _ in range(len(similar_pairs)):
        type1, type2 = random.sample(clause_types, 2)
        if clause_groups[type1] and clause_groups[type2]:
            clause1 = random.choice(clause_groups[type1])
            clause2 = random.choice(clause_groups[type2])
            dissimilar_pairs.append({
                'text1': clause1['text'],
                'text2': clause2['text'],
                'contract1': clause1['contract'],
                'contract2': clause2['contract'],
                'clause_type1': type1,
                'clause_type2': type2,
                'label': 0,  # Dissimilar
                'similarity': random.random() * 0.4  # 0.0-0.4
            })
    
    # Combine and shuffle
    all_pairs = similar_pairs + dissimilar_pairs
    random.shuffle(all_pairs)
    
    print(f"   ✅ Created {len(similar_pairs)} similar pairs")
    print(f"   ✅ Created {len(dissimilar_pairs)} dissimilar pairs")
    print(f"   ✅ Total: {len(all_pairs)} comparison pairs")
    print()
    
    # Save dataset
    output_dir = Path("datasets/comparison")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "comparison_dataset.json"
    with open(output_file, 'w') as f:
        json.dump({
            'pairs': all_pairs,
            'statistics': {
                'total_pairs': len(all_pairs),
                'similar_pairs': len(similar_pairs),
                'dissimilar_pairs': len(dissimilar_pairs),
                'clause_types': len(clause_groups)
            }
        }, f, indent=2)
    
    print(f"✅ Dataset saved to: {output_file}")
    print(f"   Size: {len(all_pairs)} pairs")
    print()
    
    # Save clause groups for reference
    groups_file = output_dir / "clause_groups.json"
    with open(groups_file, 'w') as f:
        json.dump({k: len(v) for k, v in clause_groups.items()}, f, indent=2, sort_keys=True)
    
    print(f"✅ Clause groups saved to: {groups_file}")
    print()
    
    return all_pairs

if __name__ == "__main__":
    pairs = create_comparison_dataset()
    
    if pairs:
        print("=" * 80)
        print("SAMPLE PAIRS")
        print("=" * 80)
        print()
        
        # Show similar pair
        similar = [p for p in pairs if p['label'] == 1][0]
        print(f"SIMILAR PAIR (Similarity: {similar['similarity']:.2f}):")
        print(f"   Clause Type: {similar['clause_type']}")
        print(f"   Text 1: {similar['text1'][:100]}...")
        print(f"   Text 2: {similar['text2'][:100]}...")
        print()
        
        # Show dissimilar pair
        dissimilar = [p for p in pairs if p['label'] == 0][0]
        print(f"DISSIMILAR PAIR (Similarity: {dissimilar['similarity']:.2f}):")
        print(f"   Type 1: {dissimilar.get('clause_type1', 'N/A')}")
        print(f"   Type 2: {dissimilar.get('clause_type2', 'N/A')}")
        print(f"   Text 1: {dissimilar['text1'][:100]}...")
        print(f"   Text 2: {dissimilar['text2'][:100]}...")
        print()
