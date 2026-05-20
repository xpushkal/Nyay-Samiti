from __future__ import annotations

import os
# Force CPU and disable MPS completely to avoid memory issues
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from pathlib import Path
from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, Trainer, TrainingArguments
import torch

DATA_DIR = Path("model_development/datasets/LegalNER_full/InLegalNER/prepared")
MODEL = "nlpaueb/legal-bert-base-uncased"
OUT   = Path("checkpoints/legalbert_inlegalner")

def collect_tags(ds):
    tags = set()
    for split in ds.keys():
        if ds.get(split):
            for row in ds[split]["ner_tags"]:
                for t in row:
                    tags.add(t)
    tags = sorted(list(tags))
    id2label = {i:t for i,t in enumerate(tags)}
    label2id = {t:i for i,t in id2label.items()}
    return id2label, label2id

def encode_labels(batch, label2id):
    batch["labels"] = [[label2id.get(t, 0) for t in row] for row in batch["ner_tags"]]
    batch.pop("ner_tags")
    return batch

def main():
    # Force CPU only - disable all GPU/MPS to avoid memory issues
    device = torch.device("cpu")
    print(f"Using device: {device} (CPU only - MPS disabled for stability)")
    
    ds = load_from_disk(str(DATA_DIR))
    tok = AutoTokenizer.from_pretrained(MODEL)
    id2label, label2id = collect_tags(ds)
    ds = ds.map(lambda b: encode_labels(b, label2id), batched=True)
    collator = DataCollatorForTokenClassification(tokenizer=tok)
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL, 
        num_labels=len(id2label), 
        id2label=id2label, 
        label2id=label2id
    )
    # Explicitly move model to CPU and ensure it stays there
    model = model.to(device)
    model = model.cpu()  # Double ensure CPU

    # Check if validation or test set exists
    eval_dataset = ds.get("validation") or ds.get("test")
    eval_strategy = "steps" if eval_dataset else "no"
    
    args = TrainingArguments(
        output_dir=str(OUT),
        per_device_train_batch_size=8,  # Reduced to avoid memory issues
        per_device_eval_batch_size=8,   # Smaller eval batch
        learning_rate=5e-5,
        num_train_epochs=2,
        eval_strategy=eval_strategy,
        save_strategy="epoch",
        logging_steps=50,
        report_to="none",
        max_grad_norm=1.0,
        dataloader_num_workers=0,  # Avoid multiprocessing
        use_cpu=True,  # Force CPU
        no_cuda=True   # Disable CUDA
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds.get("train"),
        eval_dataset=eval_dataset,
        tokenizer=tok,
        data_collator=collator
    )
    trainer.train()
    trainer.save_model(str(OUT))
    tok.save_pretrained(str(OUT))
    print(f"[+] Saved NER model to {OUT}")

if __name__ == "__main__":
    main()
