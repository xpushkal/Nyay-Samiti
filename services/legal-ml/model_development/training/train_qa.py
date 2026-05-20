"""
Train Question Answering Model
Trains a BERT model for extractive QA on legal documents
"""

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

import json
import torch
from transformers import (
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    default_data_collator
)
from datasets import Dataset
import evaluate
import numpy as np

print("=" * 80)
print("🚀 TRAINING LEGAL QA MODEL")
print("=" * 80)

# Load datasets
train_path = "model_development/datasets/qa/train.json"
dev_path = "model_development/datasets/qa/dev.json"

print(f"\n📂 Loading datasets...")
print(f"   Train: {train_path}")
print(f"   Dev: {dev_path}")

with open(train_path, 'r') as f:
    train_data = json.load(f)["data"]

with open(dev_path, 'r') as f:
    dev_data = json.load(f)["data"]

print(f"✅ Loaded datasets")

# Convert to flat format
def extract_examples(data):
    """Extract QA examples from SQuAD format"""
    examples = []
    for article in data:
        for paragraph in article["paragraphs"]:
            context = paragraph["context"]
            question = paragraph["question"]
            answers = paragraph["answers"]
            qa_id = paragraph["id"]
            
            answer_text = answers["text"][0] if isinstance(answers["text"], list) else answers["text"]
            answer_start = answers["answer_start"][0] if isinstance(answers["answer_start"], list) else answers["answer_start"]
            
            examples.append({
                "id": qa_id,
                "question": question,
                "context": context,
                "answer_text": answer_text,
                "answer_start": answer_start
            })
    return examples

train_examples = extract_examples(train_data)
dev_examples = extract_examples(dev_data)

print(f"\n📊 Dataset size:")
print(f"   Training: {len(train_examples)} examples")
print(f"   Validation: {len(dev_examples)} examples")

# Create datasets
train_dataset = Dataset.from_list(train_examples)
dev_dataset = Dataset.from_list(dev_examples)

# Initialize model and tokenizer
model_name = "nlpaueb/legal-bert-base-uncased"  # Legal BERT for legal domain
print(f"\n🔧 Loading model: {model_name}")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"✅ Model loaded on {device}")

# Tokenization function
def preprocess_function(examples):
    """Tokenize examples for QA"""
    questions = examples["question"]
    contexts = examples["context"]
    answers = examples["answer_text"]
    starts = examples["answer_start"]
    
    # Tokenize
    tokenized_examples = tokenizer(
        questions,
        contexts,
        max_length=384,
        truncation="only_second",
        padding="max_length",
        return_offsets_mapping=True
    )
    
    # Find start and end positions
    start_positions = []
    end_positions = []
    
    for i, (offset, answer, start) in enumerate(zip(
        tokenized_examples["offset_mapping"], answers, starts
    )):
        # Find the start and end of the answer in the tokenized context
        answer_end = start + len(answer)
        
        # Find which tokens correspond to the answer
        token_start_index = 0
        token_end_index = len(offset) - 1
        
        # Find start position
        for idx, (offset_start, offset_end) in enumerate(offset):
            if offset_start <= start < offset_end:
                token_start_index = idx
                break
        
        # Find end position
        for idx, (offset_start, offset_end) in enumerate(offset):
            if offset_start < answer_end <= offset_end:
                token_end_index = idx
                break
        
        start_positions.append(token_start_index)
        end_positions.append(token_end_index)
    
    tokenized_examples["start_positions"] = start_positions
    tokenized_examples["end_positions"] = end_positions
    
    # Remove offset_mapping (not needed for training)
    tokenized_examples.pop("offset_mapping")
    
    return tokenized_examples

# Tokenize datasets
print("\n🔄 Tokenizing datasets...")
train_dataset = train_dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=train_dataset.column_names
)
dev_dataset = dev_dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dev_dataset.column_names
)
print("✅ Tokenization complete")

# Training arguments
output_dir = "checkpoints/legalbert_qa"
print(f"\n⚙️  Setting up training configuration...")
print(f"   Output directory: {output_dir}")

training_args = TrainingArguments(
    output_dir=output_dir,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    logging_steps=100,
    report_to="none",
    use_mps_device=True if device == "mps" else False,
    fp16=False
)

# Metrics
def compute_metrics(eval_pred):
    """Compute exact match and F1 score"""
    predictions, labels = eval_pred
    
    # predictions are (start_logits, end_logits)
    start_logits, end_logits = predictions
    
    # Get predicted start and end positions
    start_preds = np.argmax(start_logits, axis=1)
    end_preds = np.argmax(end_logits, axis=1)
    
    # Get true positions
    start_true = labels[0]
    end_true = labels[1]
    
    # Calculate exact match
    exact_match = np.mean((start_preds == start_true) & (end_preds == end_true))
    
    # Calculate position accuracy
    start_acc = np.mean(start_preds == start_true)
    end_acc = np.mean(end_preds == end_true)
    
    return {
        "exact_match": exact_match,
        "start_accuracy": start_acc,
        "end_accuracy": end_acc
    }

# Initialize trainer
print("\n🏋️  Initializing trainer...")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset,
    tokenizer=tokenizer,
    data_collator=default_data_collator,
    compute_metrics=compute_metrics
)

print("\n" + "=" * 80)
print("🚀 STARTING TRAINING")
print("=" * 80)
print(f"   Training samples: {len(train_dataset)}")
print(f"   Validation samples: {len(dev_dataset)}")
print(f"   Batch size: {training_args.per_device_train_batch_size}")
print(f"   Epochs: {training_args.num_train_epochs}")
print(f"   Learning rate: {training_args.learning_rate}")
print(f"\n   ⏱️  Estimated time: ~2-3 hours on MPS")
print("=" * 80 + "\n")

# Train
trainer.train()

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)

# Save final model
final_path = os.path.join(output_dir, "final")
print(f"\n💾 Saving final model to: {final_path}")
trainer.save_model(final_path)
tokenizer.save_pretrained(final_path)
print("✅ Model saved")

# Final evaluation
print("\n📈 Running final evaluation...")
eval_results = trainer.evaluate()

print("\n" + "=" * 80)
print("📊 FINAL EVALUATION RESULTS")
print("=" * 80)
print(f"   Eval Loss: {eval_results['eval_loss']:.4f}")
print(f"   Exact Match: {eval_results['eval_exact_match']:.2%}")
print(f"   Start Accuracy: {eval_results['eval_start_accuracy']:.2%}")
print(f"   End Accuracy: {eval_results['eval_end_accuracy']:.2%}")

# Test on a few examples
print("\n" + "=" * 80)
print("🧪 SAMPLE PREDICTIONS")
print("=" * 80)

test_examples = [
    {
        "question": "What is the governing law?",
        "context": "This Agreement shall be governed by and construed in accordance with the laws of the State of California."
    },
    {
        "question": "What is the termination notice period?",
        "context": "Either party may terminate this Agreement upon thirty (30) days' prior written notice to the other party."
    },
    {
        "question": "What is the limitation of liability?",
        "context": "In no event shall either party's total liability exceed the amount of fees paid under this Agreement."
    }
]

for i, example in enumerate(test_examples, 1):
    print(f"\n{i}. Question: {example['question']}")
    print(f"   Context: {example['context'][:80]}...")
    
    inputs = tokenizer(
        example["question"],
        example["context"],
        return_tensors="pt",
        max_length=384,
        truncation="only_second"
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    start_idx = torch.argmax(outputs.start_logits)
    end_idx = torch.argmax(outputs.end_logits)
    
    answer_tokens = inputs["input_ids"][0][start_idx:end_idx+1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)
    
    print(f"   Answer: {answer}")

print("\n" + "=" * 80)
print("✅ Training complete! Model ready for integration.")
print(f"   Model location: {final_path}")
print("=" * 80)
