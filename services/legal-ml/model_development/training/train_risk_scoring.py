#!/usr/bin/env python3
"""
Train Risk Scoring Model for Contract Clauses
Predicts risk severity (1-10) for legal contract clauses
"""

import os
import sys
import json
from pathlib import Path
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Configuration
BASE_MODEL = "nlpaueb/legal-bert-base-uncased"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "checkpoints" / "legalbert_risk_scorer"
DATASET_FILE = Path(__file__).parent.parent / "datasets" / "risk_scoring" / "risk_dataset.json"
MAX_LENGTH = 512
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
EPOCHS = 3
NUM_LABELS = 10  # Risk scores from 1-10

def main():
    print("=" * 80)
    print("RISK SCORING MODEL TRAINING")
    print("Predicting Contract Clause Risk Severity (1-10)")
    print("=" * 80)
    print()
    
    # Device setup
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🖥️  Device: {device}")
    print()
    
    # Load dataset
    print(f"📥 Loading risk scoring dataset...")
    if not DATASET_FILE.exists():
        print(f"❌ Dataset not found at {DATASET_FILE}")
        print(f"   Run: python datasets/prepare_risk_dataset.py")
        sys.exit(1)
    
    with open(DATASET_FILE, 'r') as f:
        data = json.load(f)
    
    examples = data['examples']
    print(f"   ✅ Loaded {len(examples)} examples")
    print()
    
    # Show statistics
    stats = data['statistics']
    print(f"📊 Dataset Statistics:")
    print(f"   Total examples: {stats['total_examples']}")
    print(f"   Risk distribution:")
    for level, count in stats['risk_distribution'].items():
        pct = count / stats['total_examples'] * 100
        print(f"      {level.upper():<10}: {count:>5} ({pct:>5.1f}%)")
    print()
    
    # Prepare data for training
    print(f"🔄 Preparing training data...")
    texts = [ex['text'] for ex in examples]
    # Convert risk scores to 0-indexed labels (1-10 -> 0-9)
    labels = [ex['risk_score'] - 1 for ex in examples]
    
    # Split data
    train_texts, eval_texts, train_labels, eval_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"   Training examples: {len(train_texts)}")
    print(f"   Evaluation examples: {len(eval_texts)}")
    print()
    
    # Load tokenizer and model
    print(f"📦 Loading model and tokenizer...")
    print(f"   Base model: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL,
        num_labels=NUM_LABELS,
        problem_type="single_label_classification"
    )
    print(f"   ✅ Model loaded")
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")
    print()
    
    # Tokenize data
    print(f"🔄 Tokenizing data...")
    
    def tokenize_function(texts):
        return tokenizer(
            texts,
            padding="max_length",
            truncation=True,
            max_length=MAX_LENGTH
        )
    
    train_encodings = tokenize_function(train_texts)
    eval_encodings = tokenize_function(eval_texts)
    
    # Create datasets
    train_dataset = Dataset.from_dict({
        **train_encodings,
        'labels': train_labels
    })
    eval_dataset = Dataset.from_dict({
        **eval_encodings,
        'labels': eval_labels
    })
    
    print(f"   ✅ Tokenization complete")
    print()
    
    # Define metrics
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        # Get predicted classes
        preds = np.argmax(predictions, axis=1)
        
        # Convert back to 1-10 scale
        preds_scaled = preds + 1
        labels_scaled = labels + 1
        
        # Calculate metrics
        mae = mean_absolute_error(labels_scaled, preds_scaled)
        mse = mean_squared_error(labels_scaled, preds_scaled)
        rmse = np.sqrt(mse)
        
        # Calculate accuracy (exact match)
        accuracy = np.mean(preds == labels)
        
        # Calculate accuracy within ±1
        accuracy_1 = np.mean(np.abs(preds - labels) <= 1)
        
        # Calculate accuracy within ±2
        accuracy_2 = np.mean(np.abs(preds - labels) <= 2)
        
        return {
            'accuracy': accuracy,
            'accuracy_within_1': accuracy_1,
            'accuracy_within_2': accuracy_2,
            'mae': mae,
            'rmse': rmse,
        }
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        eval_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=EPOCHS,
        weight_decay=0.01,
        save_total_limit=2,
        logging_dir=str(OUTPUT_DIR / "logs"),
        logging_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy_within_1",
        greater_is_better=True,
        fp16=False,  # MPS doesn't support fp16
        report_to=["tensorboard"],
        push_to_hub=False,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )
    
    print("=" * 80)
    print("🚀 STARTING TRAINING")
    print("=" * 80)
    print(f"   Training samples: {len(train_dataset)}")
    print(f"   Evaluation samples: {len(eval_dataset)}")
    print(f"   Batch size: {BATCH_SIZE}")
    print(f"   Epochs: {EPOCHS}")
    print(f"   Learning rate: {LEARNING_RATE}")
    print()
    print(f"   Expected steps per epoch: {len(train_dataset) // BATCH_SIZE}")
    print(f"   Total expected steps: {(len(train_dataset) // BATCH_SIZE) * EPOCHS}")
    print()
    print(f"   ⏱️  Estimated time: ~30-40 minutes on MPS")
    print("=" * 80)
    print()
    
    # Train!
    try:
        train_result = trainer.train()
        
        print()
        print("=" * 80)
        print("✅ TRAINING COMPLETE!")
        print("=" * 80)
        print()
        print(f"📊 Training metrics:")
        print(f"   Training loss: {train_result.metrics['train_loss']:.4f}")
        print(f"   Training runtime: {train_result.metrics['train_runtime']:.2f}s")
        print(f"   Steps per second: {train_result.metrics['train_steps_per_second']:.2f}")
        print()
        
        # Save final model
        print(f"💾 Saving final model...")
        trainer.save_model(str(OUTPUT_DIR / "final"))
        tokenizer.save_pretrained(str(OUTPUT_DIR / "final"))
        
        # Save label mapping
        label_map = {str(i): i+1 for i in range(NUM_LABELS)}  # 0->1, 1->2, ..., 9->10
        with open(OUTPUT_DIR / "final" / "label_map.json", 'w') as f:
            json.dump({"id2score": label_map, "num_labels": NUM_LABELS}, f, indent=2)
        
        print(f"   ✅ Model saved to: {OUTPUT_DIR / 'final'}")
        print()
        
        # Final evaluation
        print(f"📈 Running final evaluation...")
        eval_results = trainer.evaluate()
        
        print()
        print("=" * 80)
        print("📊 FINAL EVALUATION RESULTS")
        print("=" * 80)
        print(f"   Exact Accuracy: {eval_results['eval_accuracy']:.2%}")
        print(f"   Accuracy (±1): {eval_results['eval_accuracy_within_1']:.2%}")
        print(f"   Accuracy (±2): {eval_results['eval_accuracy_within_2']:.2%}")
        print(f"   Mean Absolute Error: {eval_results['eval_mae']:.2f}")
        print(f"   Root Mean Squared Error: {eval_results['eval_rmse']:.2f}")
        print()
        
        print("✅ Training complete! Model ready for integration.")
        print(f"   Best checkpoint: {OUTPUT_DIR}")
        print()
        
    except KeyboardInterrupt:
        print()
        print("⚠️  Training interrupted by user")
        print(f"   Checkpoints saved in: {OUTPUT_DIR}")
    except Exception as e:
        print()
        print(f"❌ Training error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
