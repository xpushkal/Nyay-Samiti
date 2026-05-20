"""
Train CUAD Clause Classifier from Scratch
Simple and reliable approach using base LegalBERT
"""

import torch
import json
import logging
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_cuad_data(cuad_path):
    """Load and extract clause data from CUAD"""
    logger.info(f"Loading CUAD data from {cuad_path}...")
    
    with open(cuad_path) as f:
        data = json.load(f)
    
    texts = []
    labels = []
    label_set = set()
    
    for doc in data['data']:
        for para in doc['paragraphs']:
            context = para['context']
            
            for qa in para['qas']:
                if qa.get('is_impossible', False) or not qa.get('answers'):
                    continue
                
                # Extract clause type from question
                question = qa['question']
                
                # Parse: "Highlight the parts (if any) of this contract related to "Document Name""
                if 'related to' in question:
                    clause_type = question.split('related to')[-1].strip(' ".\n')
                elif 'regarding' in question:
                    clause_type = question.split('regarding')[-1].strip(' ".\n')
                else:
                    clause_type = question[:50]
                
                # Get answer text
                for answer in qa['answers']:
                    text = answer['text'].strip()
                    if len(text) > 20:  # Only meaningful clauses
                        texts.append(text)
                        labels.append(clause_type)
                        label_set.add(clause_type)
    
    logger.info(f"Extracted {len(texts)} clauses across {len(label_set)} types")
    
    # Create label mapping
    sorted_labels = sorted(list(label_set))
    label2id = {label: idx for idx, label in enumerate(sorted_labels)}
    id2label = {idx: label for label, idx in label2id.items()}
    
    # Convert labels to IDs
    label_ids = [label2id[label] for label in labels]
    
    return texts, label_ids, label2id, id2label


def compute_metrics(eval_pred):
    """Compute accuracy and F1 for multi-class classification"""
    predictions, labels = eval_pred
    preds = predictions.argmax(-1)
    
    accuracy = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average='weighted')
    
    return {
        'accuracy': accuracy,
        'f1': f1
    }


def main():
    print("=" * 80)
    print("CUAD CLAUSE CLASSIFIER - TRAINING FROM SCRATCH")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    
    # Paths
    cuad_path = base_dir / 'model_development/datasets/CUAD_full/CUAD_v1.json'
    base_model_path = base_dir / 'checkpoints/legalbert'
    output_dir = base_dir / 'checkpoints/legalbert_cuad_improved'
    
    # Check paths
    if not cuad_path.exists():
        logger.error(f"CUAD data not found: {cuad_path}")
        return
    
    if not base_model_path.exists():
        logger.error(f"Base model not found: {base_model_path}")
        return
    
    # Load data
    texts, labels, label2id, id2label = load_cuad_data(cuad_path)
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    logger.info(f"Train: {len(train_texts)}, Val: {len(val_texts)}")
    
    # Load tokenizer
    logger.info(f"Loading tokenizer from {base_model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(str(base_model_path))
    
    # Tokenize
    logger.info("Tokenizing data...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)
    
    # Create datasets
    train_dataset = Dataset.from_dict({
        **train_encodings,
        'labels': train_labels
    })
    val_dataset = Dataset.from_dict({
        **val_encodings,
        'labels': val_labels
    })
    
    # Load model
    logger.info(f"Loading model from {base_model_path}...")
    model = AutoModelForSequenceClassification.from_pretrained(
        str(base_model_path),
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=str(output_dir / 'logs'),
        logging_steps=100,
        eval_strategy='steps',
        eval_steps=500,
        save_strategy='steps',
        save_steps=500,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model='f1',
        greater_is_better=True,
        report_to='none',
        use_mps_device=torch.backends.mps.is_available()
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )
    
    # Train
    logger.info("\n🚀 Starting training...")
    trainer.train()
    
    # Save
    logger.info(f"\n💾 Saving model to {output_dir}...")
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    
    # Save label mapping
    with open(output_dir / 'label_map.json', 'w') as f:
        json.dump({
            'label2id': label2id,
            'id2label': id2label,
            'num_labels': len(label2id)
        }, f, indent=2)
    
    # Evaluate
    logger.info("\n📊 Final evaluation...")
    results = trainer.evaluate()
    
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETE")
    print("=" * 80)
    print(f"Accuracy: {results['eval_accuracy']:.2%}")
    print(f"F1 Score: {results['eval_f1']:.2%}")
    print(f"Model saved to: {output_dir}")
    print("=" * 80)


if __name__ == '__main__':
    main()
