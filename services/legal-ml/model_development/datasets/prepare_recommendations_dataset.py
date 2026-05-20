#!/usr/bin/env python3
"""
Prepare Clause Recommendations Dataset
Creates clause improvement/alternative pairs
"""

import json
from pathlib import Path
import random

# Clause improvement templates
CLAUSE_IMPROVEMENTS = {
    "Termination For Convenience": [
        {
            "original": "Either party may terminate this agreement at any time.",
            "improved": "Either party may terminate this Agreement upon thirty (30) days' prior written notice to the other party.",
            "reason": "Added specific notice period requirement"
        },
        {
            "original": "We can end this whenever we want.",
            "improved": "Either party may terminate this Agreement for convenience upon ninety (90) days' written notice.",
            "reason": "Professional language with clear termination process"
        }
    ],
    "Confidentiality": [
        {
            "original": "You must keep information confidential.",
            "improved": "Receiving Party agrees to hold and maintain all Confidential Information in strictest confidence and shall not disclose such information to any third party without prior written consent.",
            "reason": "Specific obligations and third-party disclosure restrictions"
        }
    ],
    "Limitation of Liability": [
        {
            "original": "Company is not liable for damages.",
            "improved": "In no event shall either party's total liability exceed the amount of fees paid under this Agreement in the twelve (12) months preceding the claim, except for breaches of confidentiality or willful misconduct.",
            "reason": "Cap on liability with exceptions for serious breaches"
        }
    ],
    "Non-Compete": [
        {
            "original": "You can't compete with us.",
            "improved": "During the term of this Agreement and for a period of twelve (12) months thereafter, within a fifty (50) mile radius, Employee shall not directly or indirectly engage in any business that competes with Company's core business.",
            "reason": "Limited scope: time-bound, geography-bound, and specific to core business"
        }
    ],
    "Governing Law": [
        {
            "original": "California law applies.",
            "improved": "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of laws principles.",
            "reason": "Formal language excluding conflict of laws complications"
        }
    ]
}

def create_recommendations_dataset():
    """Create clause recommendations dataset"""
    
    print("=" * 80)
    print("CREATING CLAUSE RECOMMENDATIONS DATASET")
    print("=" * 80)
    print()
    
    # Load CUAD for more examples
    cuad_file = Path("datasets/CUAD_full/CUAD_v1.json")
    
    examples = []
    
    # Add template examples
    for clause_type, improvements in CLAUSE_IMPROVEMENTS.items():
        for imp in improvements:
            examples.append({
                'original': imp['original'],
                'improved': imp['improved'],
                'clause_type': clause_type,
                'improvement_type': 'rewrite',
                'reason': imp['reason']
            })
    
    print(f"📊 Dataset Statistics:")
    print(f"   Template examples: {len(examples)}")
    
    # Load CUAD and create variations
    if cuad_file.exists():
        print(f"📂 Loading CUAD for augmentation...")
        with open(cuad_file, 'r') as f:
            cuad_data = json.load(f)
        
        # Extract some clauses and create synthetic improvements
        clause_count = 0
        for doc in cuad_data['data'][:50]:  # Sample first 50 docs
            for para in doc['paragraphs']:
                for qa in para['qas']:
                    if qa.get('is_impossible', False) or not qa.get('answers'):
                        continue
                    
                    import re
                    match = re.search(r'"([^"]+)"', qa['question'])
                    if not match:
                        continue
                    
                    clause_type = match.group(1)
                    
                    for answer in qa['answers'][:1]:  # First answer only
                        text = answer['text'].strip()
                        if len(text) > 50 and len(text) < 500:
                            # Create synthetic improvement (add standard protective language)
                            improved = text
                            if "subject to" not in text.lower():
                                improved = f"Subject to the terms and conditions of this Agreement, {text}"
                            
                            examples.append({
                                'original': text,
                                'improved': improved,
                                'clause_type': clause_type,
                                'improvement_type': 'add_conditions',
                                'reason': 'Added conditional language for clarity'
                            })
                            clause_count += 1
                            
                            if clause_count >= 100:  # Limit to 100 augmented examples
                                break
                    if clause_count >= 100:
                        break
                if clause_count >= 100:
                    break
            if clause_count >= 100:
                break
        
        print(f"   CUAD augmented examples: {clause_count}")
    
    print(f"   Total examples: {len(examples)}")
    print()
    
    # Save dataset
    output_dir = Path("datasets/recommendations")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "recommendations_dataset.json"
    with open(output_file, 'w') as f:
        json.dump({
            'examples': examples,
            'statistics': {
                'total_examples': len(examples),
                'clause_types': len(set(ex['clause_type'] for ex in examples)),
                'improvement_types': list(set(ex['improvement_type'] for ex in examples))
            }
        }, f, indent=2)
    
    print(f"✅ Dataset saved to: {output_file}")
    print(f"   Size: {len(examples)} examples")
    print()
    
    return examples

if __name__ == "__main__":
    examples = create_recommendations_dataset()
    
    if examples:
        print("=" * 80)
        print("SAMPLE EXAMPLES")
        print("=" * 80)
        print()
        
        for i, ex in enumerate(examples[:3], 1):
            print(f"{i}. {ex['clause_type']}")
            print(f"   Original: {ex['original'][:100]}...")
            print(f"   Improved: {ex['improved'][:100]}...")
            print(f"   Reason: {ex['reason']}")
            print()
