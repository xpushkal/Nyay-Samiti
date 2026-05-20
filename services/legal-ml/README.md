# 🏛️ Nyay-Samiti Legal AI

> Advanced Legal Document Analysis powered by 7 fine-tuned ML models

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Features

Nyay-Samiti provides **7 state-of-the-art ML models** for comprehensive legal document analysis:

| Model | Purpose | Performance | API Endpoint |
|-------|---------|-------------|--------------|
| **NER** | Extract 29 legal entities | 90%+ accuracy | `/api/ner/*` |
| **CUAD Classifier** | Classify 41 clause types | 77.59% accuracy | `/api/classification/*` |
| **Summarization** | Generate document summaries | ROUGE-1: 56.81% | `/api/summarize` |
| **Risk Scoring** | Assess contract risk (1-10 scale) | 84.16% accuracy | `/api/risk/*` |
| **Comparison** | Find similar clauses | MAE: 0.24 | `/api/compare/*` |
| **Recommendations** | Improve clause language | ROUGE: 99.88% | `/api/recommendations/*` |
| **QA** | Answer legal questions | 87.18% accuracy | `/api/qa/*` |

### 🆕 **NEW: Backend Integration API**

**Complete Document Analysis** - Process documents through all 7 models in one request:

```bash
POST /api/analyze/complete
```

**Returns structured JSON ready for backend storage:**
- ✅ Classified clauses
- ✅ Extracted entities
- ✅ Risk assessment
- ✅ Document summary
- ✅ Question answering
- ✅ UUID tracking
- ✅ Processing metadata

See [**BACKEND_INTEGRATION_GUIDE.md**](BACKEND_INTEGRATION_GUIDE.md) for complete integration examples!

## 📦 Quick Start

### Prerequisites
- Python 3.11+
- 8GB+ RAM
- ~5GB disk space for trimmed inference checkpoints

### Installation

```bash
# Clone repository
git clone https://github.com/xpushkal/legal-nlp.git
cd nyay-samiti

# Create virtual environment
python3.11 -m venv venv_py311
source venv_py311/bin/activate  # On Windows: venv_py311\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
# Start FastAPI server
uvicorn main:app --reload

# Access API documentation
open http://localhost:8000/docs
```

## 📁 Project Structure

```
nyay-samiti/
├── app/                          # Main application
│   ├── api/                      # API routes (7 ML endpoints)
│   ├── core/                     # Core utilities
│   ├── models/                   # Pydantic models
│   └── services/                 # ML service classes
│       ├── ner/                  # Named Entity Recognition
│       ├── classification/       # Clause Classification
│       ├── summarization/        # Document Summarization
│       ├── risk/                 # Risk Assessment
│       ├── comparison/           # Clause Comparison
│       ├── recommendations/      # Clause Improvements
│       └── qa/                   # Question Answering
│
├── checkpoints/                  # Trained model weights
│   ├── legalbert/               # NER model
│   ├── legalbert_cuad/          # Classifier
│   ├── bart_billsum_finetuned/  # Summarization
│   ├── legalbert_risk_scorer/   # Risk scoring
│   ├── legal_comparison_model/  # Comparison
│   ├── t5_recommendations/      # Recommendations
│   └── legalbert_qa/            # QA model
│
├── configs/                      # Configuration files
├── model_development/            # Model training and datasets
│   ├── datasets/                 # Dataset preparation scripts
│   └── training/                 # Model training scripts
├── tests/                        # Integration & unit tests
├── docs/                         # Documentation
└── main.py                       # FastAPI application
```

## 🎯 API Usage Examples

### 1. Named Entity Recognition

```bash
curl -X POST "http://localhost:8000/api/ner/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "This Agreement is entered into on January 1, 2024 between ABC Corp and XYZ Ltd."}'
```

### 2. Clause Classification

```bash
curl -X POST "http://localhost:8000/api/classification/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "Either party may terminate this agreement with 30 days written notice."}'
```

### 3. Risk Assessment

```bash
curl -X POST "http://localhost:8000/api/risk/score" \
  -H "Content-Type: application/json" \
  -d '{"text": "The party shall have unlimited liability for any damages."}'
```

### 4. Clause Recommendations

```bash
curl -X POST "http://localhost:8000/api/recommendations/improve" \
  -H "Content-Type: application/json" \
  -d '{"clause": "Party can terminate anytime."}'
```

### 5. Legal Question Answering

```bash
curl -X POST "http://localhost:8000/api/qa/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the governing law?",
    "context": "This agreement shall be governed by the laws of New York."
  }'
```

## 🧪 Testing

```bash
# Run all integration tests
export PYTHONPATH=$(pwd)
python tests/integration/test_ner_integration.py
python tests/integration/test_cuad_integration.py
python tests/integration/test_summarization_integration.py
python tests/integration/test_risk_integration.py
python tests/integration/test_comparison_integration.py
python tests/integration/test_recommendations_integration.py
python tests/integration/test_qa_integration.py

# Or use pytest (when installed)
pytest tests/integration/
```

## 🔗 Backend Integration

Nyay-Samiti provides a comprehensive backend integration API for seamless data flow.

### Complete Document Analysis

Process documents through all 7 models in one request:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze/complete",
    json={
        "text": "Your contract text here...",
        "document_id": "contract_001",
        "questions": ["What is the payment term?"],
        "summary_length": 150
    }
)

result = response.json()
# Returns structured JSON with:
# - clauses, entities, risks, summary, qa_results
# - UUID for tracking
# - Model versions and metadata
```

### Batch Processing

Process multiple documents asynchronously:

```python
response = requests.post(
    "http://localhost:8000/api/analyze/batch",
    json={
        "documents": [
            {"text": "Contract 1...", "document_id": "doc_001"},
            {"text": "Contract 2...", "document_id": "doc_002"}
        ],
        "callback_url": "https://your-backend.com/api/callback"
    }
)

job_id = response.json()["job_id"]
# Check status: GET /api/analyze/batch/{job_id}
```

### Configuration

Set environment variables for automatic backend integration:

```bash
export BACKEND_URL="http://your-backend.com/api"
export BACKEND_API_KEY="your-api-key"
```

### Complete Documentation

- 📖 **[Backend Integration Guide](BACKEND_INTEGRATION_GUIDE.md)** - Complete guide with examples
- 💡 **[Integration Summary](BACKEND_INTEGRATION_COMPLETE.md)** - Quick start guide
- 🔧 **[Example Code](examples/backend_integration_example.py)** - Working examples
- 🧪 **Test**: Run `python3 test_backend_integration.py`

## 🎓 Training Models

All models are pre-trained and ready to use. To retrain:

```bash
# Prepare datasets
python model_development/datasets/prepare_cuad.py
python model_development/datasets/prepare_inlegalner.py
python model_development/datasets/prepare_risk_dataset.py
python model_development/datasets/prepare_comparison_dataset.py
python model_development/datasets/prepare_recommendations_dataset.py
python model_development/datasets/prepare_qa_dataset.py

# Train models
python model_development/training/train_ner_hf.py
python model_development/training/train_classifier_cuad.py
python model_development/training/train_summarization.py
python model_development/training/train_risk_scoring.py
python model_development/training/train_comparison.py
python model_development/training/train_recommendations.py
python model_development/training/train_qa.py
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key settings:
- `API_HOST` - API server host (default: 0.0.0.0)
- `API_PORT` - API server port (default: 8000)
- `CHECKPOINT_DIR` - Model checkpoints directory
- `LOG_LEVEL` - Logging level (INFO, DEBUG, etc.)
- `BACKEND_URL` - Your backend API URL (for auto-send)
- `BACKEND_API_KEY` - Backend authentication key

## 📊 Model Performance

| Model | Metric | Score |
|-------|--------|-------|
| NER | F1 Score | 90%+ |
| CUAD Classifier | Accuracy | 77.59% |
| Summarization | ROUGE-1 | 56.81% |
| Risk Scoring | Accuracy | 84.16% |
| Comparison | MAE | 0.24 |
| Recommendations | ROUGE-1 | 99.88% |
| QA | Start Accuracy | 87.18% |

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- **CUAD Dataset** - Contract Understanding Atticus Dataset
- **InLegalNER** - Indian Legal NER Dataset
- **LegalBERT** - Pre-trained legal language model
- **Hugging Face** - Transformers library

## 📧 Contact

- GitHub: [@xpushkal](https://github.com/xpushkal)
- Project: [legal-nlp](https://github.com/xpushkal/legal-nlp)

---

**Built with ❤️ for the legal tech community**
