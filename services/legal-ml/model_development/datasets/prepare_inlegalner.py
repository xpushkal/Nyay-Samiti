# Convert InLegalNER HF dataset into token-classification training rows for transformers
import os, sys
from pathlib import Path
from datasets import load_from_disk, DatasetDict
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent / "LegalNER_full" / "InLegalNER"
OUT  = ROOT / "prepared"
MODEL = "nlpaueb/legal-bert-base-uncased"

def to_bio(example, tokenizer):
    text = example["data"]["text"]
    anns = example.get("annotations", [])
    entities = []
    for group in anns:
        for item in group.get("result", []):
            v = item.get("value") or {}
            start = v.get("start"); end = v.get("end"); label = (v.get("labels") or ["ENT"])[0]
            if start is not None and end is not None:
                entities.append((start, end, label))
    entities.sort(key=lambda x: x[0])

    enc = tokenizer(text, return_offsets_mapping=True, truncation=True, max_length=512)
    tags = ["O"] * len(enc["offset_mapping"])
    for (s, e, label) in entities:
        found_b = False
        for i, (ts, te) in enumerate(enc["offset_mapping"]):
            if te <= s or ts >= e:
                continue
            if ts >= s and te <= e:
                if not found_b and tags[i] == "O":
                    tags[i] = f"B-{label}"
                    found_b = True
                else:
                    tags[i] = f"I-{label}"
    enc.pop("offset_mapping")
    enc["labels"] = [0] * len(enc["input_ids"])
    enc["ner_tags"] = tags
    return enc

def main():
    ds = load_from_disk(str(ROOT))
    tok = AutoTokenizer.from_pretrained(MODEL)
    processed = {}
    for split in ("train", "validation", "test"):
        if split in ds:
            processed[split] = ds[split].map(lambda ex: to_bio(ex, tok), remove_columns=ds[split].column_names)
    DatasetDict(processed).save_to_disk(str(OUT))
    print(f"[+] Saved tokenized BIO dataset to: {OUT}")

if __name__ == "__main__":
    main()
