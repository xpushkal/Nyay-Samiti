
import os, csv
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parent / "CUAD_full"
OUT_DIR = ROOT / "prepared"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "cuad_paragraphs.csv"

def extract_paragraphs(pdf_path):
    paras = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            # split by double newline or fallback by single newline groups
            chunks = [p.strip() for p in txt.split("\n\n") if p.strip()]
            if not chunks and txt.strip():
                chunks = [p.strip() for p in txt.split("\n") if p.strip()]
            paras.extend(chunks)
    return paras

def main():
    pdf_root = ROOT / "full_contract_pdf"
    if not pdf_root.exists():
        print(f"[x] Expected {pdf_root} not found. Please unzip CUAD_v1.zip into CUAD_full/")
        return
    files = list(pdf_root.rglob("*.pdf"))
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "paragraph_idx", "text"])
        for pdf in files:
            try:
                paras = extract_paragraphs(pdf)
                for i, p in enumerate(paras):
                    w.writerow([str(pdf.relative_to(ROOT)), i, p])
            except Exception as e:
                print(f"[!] Skipping {pdf}: {e}")
    print(f"[+] Wrote paragraph CSV: {OUT_CSV}")

if __name__ == "__main__":
    main()
