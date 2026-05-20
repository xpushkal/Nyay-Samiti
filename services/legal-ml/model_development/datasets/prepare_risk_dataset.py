import json
from pathlib import Path
from collections import defaultdict

# Risk severity mapping for CUAD clause types
# Based on legal risk assessment principles
CLAUSE_RISK_MAPPING = {
    # HIGH RISK (7-10)
    "Uncapped Liability": 10,  # Maximum risk - unlimited exposure
    "Most Favored Nation": 9,   # Can force unfavorable terms
    "Covenant Not To Sue": 8,   # Waives legal rights
    "Non-Compete": 8,           # Restricts business activities
    "Anti-Assignment": 7,       # Limits flexibility
    
    # MEDIUM-HIGH RISK (5-7)
    "Exclusivity": 7,           # Limits business options
    "Change Of Control": 6,     # Can trigger termination
    "No-Solicit Of Employees": 6,  # Restricts hiring
    "No-Solicit Of Customers": 6,  # Restricts business development
    "Liquidated Damages": 6,    # Fixed penalty exposure
    "Competitive Restriction Exception": 5,
    
    # MEDIUM RISK (4-6)
    "Volume Restriction": 5,    # Limits business growth
    "Minimum Commitment": 5,    # Forces minimum purchase
    "Price Restrictions": 5,    # Limits pricing flexibility
    "Non-Transferable License": 5,  # Limits license utility
    "Termination For Convenience": 4,  # Can be terminated easily
    "Notice Period To Terminate Renewal": 4,
    
    # LOW-MEDIUM RISK (2-4)
    "Ip Ownership Assignment": 4,  # IP transfer risk
    "Joint Ip Ownership": 4,    # Shared IP complications
    "Source Code Escrow": 3,    # Minimal risk, protective
    "Audit Rights": 3,          # Compliance burden
    "Insurance": 3,             # Cost obligation
    "Post-Termination Services": 3,
    "Third Party Beneficiary": 3,
    
    # LOW RISK (1-3)
    "Irrevocable Or Perpetual License": 2,  # Can't revoke
    "Unlimited/All-You-Can-Eat-License": 2,  # Unlimited use
    "Cap On Liability": 2,      # Actually reduces risk!
    "Revenue/Profit Sharing": 2,  # Revenue-based terms
    "Rofr/Rofo/Rofn": 2,        # Rights of first refusal
    "Warranty Duration": 2,     # Time-limited warranty
    "Renewal Term": 2,          # Auto-renewal
    
    # NEUTRAL/INFORMATIONAL (0-2)
    "Governing Law": 1,         # Just specifies jurisdiction
    "Agreement Date": 1,        # Informational
    "Effective Date": 1,        # Informational
    "Expiration Date": 1,       # Informational
    "Document Name": 1,         # Informational
    "Parties": 1,               # Informational
    "Affiliate License-Licensee": 2,
    "Affiliate License-Licensor": 2,
    "License Grant": 2,         # Standard grant
    "Non-Disparagement": 2,     # Reputation protection
}

def create_risk_dataset():
    """Create risk scoring dataset from CUAD"""
    
    print("=" * 80)
    print("CREATING RISK SCORING DATASET FROM CUAD")
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
    
    # Extract clause texts with risk labels
    risk_examples = []
    clause_counts = defaultdict(int)
    
    for doc in cuad_data['data']:
        for para in doc['paragraphs']:
            context = para['context']
            
            for qa in para['qas']:
                question = qa['question']
                
                # Extract clause type from question
                # Questions are like "Highlight the parts (if any) of this contract related to \"Cap On Liability\" that should be reviewed by a lawyer."
                import re
                match = re.search(r'"([^"]+)"', question)
                if not match:
                    continue
                    
                clause_type = match.group(1)
                
                # Skip if we don't have risk mapping
                if clause_type not in CLAUSE_RISK_MAPPING:
                    continue
                
                risk_score = CLAUSE_RISK_MAPPING[clause_type]
                clause_counts[clause_type] += 1
                
                # Check if this clause exists in the contract
                has_clause = qa.get('is_impossible', False) == False and len(qa.get('answers', [])) > 0
                
                if has_clause:
                    # Extract answer text
                    for answer in qa['answers']:
                        answer_text = answer['text'].strip()
                        if answer_text and len(answer_text) > 20:  # Filter very short answers
                            risk_examples.append({
                                'text': answer_text,
                                'clause_type': clause_type,
                                'risk_score': risk_score,
                                'risk_level': get_risk_level(risk_score),
                                'contract_title': doc['title']
                            })
    
    print(f"📊 Dataset Statistics:")
    print(f"   Total examples: {len(risk_examples)}")
    print()
    
    # Show distribution
    risk_distribution = defaultdict(int)
    for ex in risk_examples:
        risk_distribution[ex['risk_level']] += 1
    
    print(f"   Risk Level Distribution:")
    for level in ['low', 'medium', 'high', 'critical']:
        count = risk_distribution[level]
        pct = count / len(risk_examples) * 100 if risk_examples else 0
        print(f"      {level.upper():<10}: {count:>5} ({pct:>5.1f}%)")
    print()
    
    # Show top clause types
    print(f"   Top 10 Clause Types:")
    sorted_clauses = sorted(clause_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for clause_type, count in sorted_clauses:
        risk = CLAUSE_RISK_MAPPING[clause_type]
        print(f"      {clause_type:<35} {count:>4} examples (risk: {risk}/10)")
    print()
    
    # Save dataset
    output_dir = Path("datasets/risk_scoring")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "risk_dataset.json"
    with open(output_file, 'w') as f:
        json.dump({
            'examples': risk_examples,
            'clause_risk_mapping': CLAUSE_RISK_MAPPING,
            'statistics': {
                'total_examples': len(risk_examples),
                'risk_distribution': dict(risk_distribution),
                'clause_counts': dict(clause_counts)
            }
        }, f, indent=2)
    
    print(f"✅ Dataset saved to: {output_file}")
    print(f"   Size: {len(risk_examples)} examples")
    print()
    
    # Save risk mapping reference
    mapping_file = output_dir / "risk_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(CLAUSE_RISK_MAPPING, f, indent=2, sort_keys=True)
    
    print(f"✅ Risk mapping saved to: {mapping_file}")
    print()
    
    return risk_examples

def get_risk_level(score):
    """Convert numeric risk score to categorical level"""
    if score >= 8:
        return 'critical'
    elif score >= 5:
        return 'high'
    elif score >= 3:
        return 'medium'
    else:
        return 'low'

if __name__ == "__main__":
    examples = create_risk_dataset()
    
    if examples:
        print("=" * 80)
        print("SAMPLE EXAMPLES")
        print("=" * 80)
        print()
        
        # Show a few examples from each risk level
        for level in ['low', 'medium', 'high', 'critical']:
            level_examples = [ex for ex in examples if ex['risk_level'] == level]
            if level_examples:
                ex = level_examples[0]
                print(f"{level.upper()} RISK EXAMPLE:")
                print(f"   Clause Type: {ex['clause_type']}")
                print(f"   Risk Score: {ex['risk_score']}/10")
                print(f"   Text: {ex['text'][:150]}...")
                print()
