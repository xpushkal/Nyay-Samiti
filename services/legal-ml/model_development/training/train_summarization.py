#!/usr/bin/env python3
"""
Fine-tune Legal Document Summarization Model
Uses BillSum dataset (US Congressional and California state bills)
Base Model: facebook/bart-large-cnn or local checkpoint
"""

import os
import sys
from pathlib import Path
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
import evaluate
import numpy as np

# Configuration
BASE_MODEL = "facebook/bart-large-cnn"
LOCAL_CHECKPOINT = Path(__file__).parent.parent.parent / "checkpoints" / "bart"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "checkpoints" / "bart_billsum_finetuned"
MAX_INPUT_LENGTH = 1024
MAX_TARGET_LENGTH = 128
BATCH_SIZE = 2  # Small batch for MPS
LEARNING_RATE = 5e-5
EPOCHS = 3
EVAL_STEPS = 500
SAVE_STEPS = 500

def main():
    print("=" * 80)
    print("LEGAL SUMMARIZATION MODEL TRAINING")
    print("Dataset: BillSum (Legal Bill Summaries)")
    print("=" * 80)
    print()
    
    # Device setup
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🖥️  Device: {device}")
    print()
    
    # Load dataset
    print("📥 Loading BillSum dataset...")
    try:
        dataset = load_dataset("billsum")
        print(f"   ✅ Loaded successfully!")
        print(f"   Train: {len(dataset['train'])} examples")
        print(f"   Test: {len(dataset['test'])} examples")
        print()
    except Exception as e:
        print(f"   ❌ Error loading dataset: {e}")
        print("   💡 Trying alternative: multi_news dataset")
        dataset = load_dataset("multi_news")
        # Rename fields to match expected format
        dataset = dataset.rename_column("document", "text")
        dataset = dataset.rename_column("summary", "summary")
        print(f"   ✅ Loaded alternative dataset!")
        print(f"   Train: {len(dataset['train'])} examples")
        print(f"   Validation: {len(dataset.get('validation', []))} examples")
        print(f"   Test: {len(dataset['test'])} examples")
        print()
    
    # Use smaller subset for faster training
    print("🔀 Using subset for training...")
    train_size = min(5000, len(dataset['train']))
    eval_size = min(500, len(dataset['test'] if 'test' in dataset else dataset.get('validation', dataset['train'])))
    
    train_dataset = dataset['train'].shuffle(seed=42).select(range(train_size))
    eval_dataset = (dataset['test'] if 'test' in dataset else 
                   dataset.get('validation', dataset['train'])).shuffle(seed=42).select(range(eval_size))
    
    print(f"   Train: {len(train_dataset)} examples")
    print(f"   Eval: {len(eval_dataset)} examples")
    print()
    
    # Load model
    print("📦 Loading model and tokenizer...")
    model_path = str(LOCAL_CHECKPOINT) if LOCAL_CHECKPOINT.exists() else BASE_MODEL
    print(f"   Model: {model_path}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        print(f"   ✅ Model loaded successfully!")
        print(f"   Parameters: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")
        print()
    except Exception as e:
        print(f"   ❌ Error loading model: {e}")
        sys.exit(1)
    
    # Preprocessing function
    def preprocess_function(examples):
        # Handle different dataset field names
        if "text" in examples:
            inputs = examples["text"]
        elif "document" in examples:
            inputs = examples["document"]
        else:
            raise ValueError("Dataset must have 'text' or 'document' field")
        
        summaries = examples["summary"]
        
        model_inputs = tokenizer(
            inputs,
            max_length=MAX_INPUT_LENGTH,
            truncation=True,
            padding="max_length"
        )
        
        labels = tokenizer(
            summaries,
            max_length=MAX_TARGET_LENGTH,
            truncation=True,
            padding="max_length"
        )
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    print("🔄 Preprocessing dataset...")
    tokenized_train = train_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=train_dataset.column_names,
        desc="Tokenizing training set"
    )
    tokenized_eval = eval_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=eval_dataset.column_names,
        desc="Tokenizing evaluation set"
    )
    print(f"   ✅ Preprocessing complete!")
    print()
    
    # Load ROUGE metric
    print("📊 Loading evaluation metric (ROUGE)...")
    rouge = evaluate.load("rouge")
    print(f"   ✅ Metric loaded!")
    print()
    
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        
        # Decode predictions
        decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
        
        # Replace -100 in labels (used for padding)
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
        
        # Compute ROUGE scores
        result = rouge.compute(
            predictions=decoded_preds,
            references=decoded_labels,
            use_stemmer=True
        )
        
        # Extract percentage scores
        result = {k: round(v * 100, 2) for k, v in result.items()}
        
        return result
    
    # Check for existing checkpoints to resume
    resume_from_checkpoint = None
    if OUTPUT_DIR.exists():
        checkpoints = sorted(OUTPUT_DIR.glob("checkpoint-*"))
        if checkpoints:
            resume_from_checkpoint = str(checkpoints[-1])
            print(f"📂 Found existing checkpoint: {checkpoints[-1].name}")
            print(f"   ✅ Will resume training from this checkpoint")
            print()
    
    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR),
        eval_strategy="steps",
        eval_steps=EVAL_STEPS,
        save_strategy="steps",
        save_steps=SAVE_STEPS,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=EPOCHS,
        weight_decay=0.01,
        save_total_limit=2,
        predict_with_generate=True,
        generation_max_length=MAX_TARGET_LENGTH,
        logging_dir=str(OUTPUT_DIR / "logs"),
        logging_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model="rouge1",
        greater_is_better=True,
        fp16=False,  # MPS doesn't support fp16
        report_to=["tensorboard"],
        push_to_hub=False,
    )
    
    # Data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    # Initialize trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    print("=" * 80)
    print("🚀 STARTING TRAINING")
    print("=" * 80)
    print(f"   Training samples: {len(tokenized_train)}")
    print(f"   Evaluation samples: {len(tokenized_eval)}")
    print(f"   Batch size: {BATCH_SIZE}")
    print(f"   Epochs: {EPOCHS}")
    print(f"   Learning rate: {LEARNING_RATE}")
    print(f"   Max input length: {MAX_INPUT_LENGTH}")
    print(f"   Max output length: {MAX_TARGET_LENGTH}")
    print()
    print("   Expected steps per epoch:", len(tokenized_train) // BATCH_SIZE)
    print("   Total expected steps:", (len(tokenized_train) // BATCH_SIZE) * EPOCHS)
    print()
    if resume_from_checkpoint:
        print(f"   🔄 Resuming from: {resume_from_checkpoint}")
        print()
    print("   ⏱️  Estimated time: ~45-60 minutes on MPS")
    print("=" * 80)
    print()
    
    # Train!
    try:
        train_result = trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        
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
        print("💾 Saving final model...")
        trainer.save_model(str(OUTPUT_DIR / "final"))
        tokenizer.save_pretrained(str(OUTPUT_DIR / "final"))
        print(f"   ✅ Model saved to: {OUTPUT_DIR / 'final'}")
        print()
        
        # Final evaluation
        print("📈 Running final evaluation...")
        eval_results = trainer.evaluate()
        
        print()
        print("=" * 80)
        print("📊 FINAL EVALUATION RESULTS")
        print("=" * 80)
        for key, value in eval_results.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.4f}")
        print()
        
        print("✅ Training complete! Model ready for integration.")
        print(f"   Best checkpoint: {OUTPUT_DIR}")
        
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
