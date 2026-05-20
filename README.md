# ⚖️ Nyay-Samiti

### AI-Powered Legal Document Analysis Platform

*Making Legal सरल — Simplifying complex legal documents with 7 fine-tuned ML models*

[![Next.js 14](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Prisma](https://img.shields.io/badge/Prisma-6.18-2D3748?logo=prisma)](https://www.prisma.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) · [Architecture](#-system-architecture) · [ML Models](#-machine-learning-pipeline) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Contributing](#-contributing)


---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Docker Deployment](#-docker-deployment)
- [Monitoring & Observability](#-monitoring--observability)
- [Testing](#-testing)
- [Configuration](#-configuration)
- [Performance Benchmarks](#-performance-benchmarks)
- [Sample Documents](#-sample-documents)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

**Nyay-Samiti** (न्याय समिति — "Justice Committee") is a full-stack AI-powered platform that transforms complex legal documents into clear, actionable insights. Upload any legal document — contracts, agreements, affidavits, court orders — and receive a comprehensive analysis powered by **7 specialized machine learning models** that extract entities, classify clauses, assess risk, generate summaries, answer questions, compare clauses, and recommend improvements.

The platform combines a **Next.js 14** frontend/backend with a **FastAPI** ML microservice, connected via REST APIs with real-time progress tracking. It is designed for legal professionals, businesses, and individuals who need to understand legal documents quickly and accurately.

### 🎯 Key Differentiators

- **7 Specialized ML Models** — Not a single generic model, but a purpose-built ensemble for legal analysis
- **Indian Legal Context** — Trained on Indian legal documents and procedures (InLegalNER dataset)
- **Real-Time Processing** — 10–15 second total analysis with live progress tracking
- **End-to-End Platform** — Upload → Analyze → Dashboard — no external tools needed
- **Production-Ready** — Docker Compose with Prometheus/Grafana monitoring

---

## ✨ Features

### 📄 Document Processing
- Upload PDF, DOC, DOCX, and TXT legal documents
- Automatic text extraction and preprocessing
- Support for 50+ legal document types (contracts, affidavits, court orders, wills, etc.)

### 🤖 AI-Powered Analysis
| Capability | Description |
|---|---|
| **Named Entity Recognition** | Extract 29 entity types (parties, dates, amounts, obligations, rights, etc.) |
| **Clause Classification** | Classify paragraphs into 41 CUAD clause types (termination, confidentiality, IP, etc.) |
| **Risk Assessment** | Score contract risk on a 0–1 scale with detailed factor analysis |
| **Document Summarization** | Generate concise executive summaries with key points |
| **Question Answering** | Ask natural language questions about your document |
| **Clause Comparison** | Measure semantic similarity between clauses |
| **Clause Recommendations** | Get AI-improved versions of problematic clauses |

### 📊 Interactive Dashboard
- Tabbed results view (Overview, Entities, Classification, Risk, Summary)
- Real-time progress tracking with animated progress bars
- Risk level indicators with color-coded badges
- Document history and analysis management

### 🔐 Security & Privacy
- End-to-end encryption (256-bit SSL)
- No permanent document storage
- GDPR-compliant data handling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Browser)                      │
│                    http://localhost:3000                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NEXT.JS APPLICATION (Port 3000)               │
│                                                                 │
│  ┌─────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  Pages       │  │  API Routes      │  │  Database Layer  │   │
│  │  /upload     │  │  /api/documents  │  │  Prisma ORM      │   │
│  │  /dashboard  │  │  /api/analysis   │  │  SQLite / PgSQL  │   │
│  │  /contact    │  │  /api/webhooks   │  │  Document Model  │   │
│  │  /how-it-works│ │  /api/metrics    │  │  Analysis Model  │   │
│  └─────────────┘  └──────────────────┘  └──────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               FASTAPI ML SERVICE (Port 8000)                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  7 ML Models:                                             │   │
│  │  LegalBERT NER │ CUAD Classifier │ BART Summarizer       │   │
│  │  Risk Scorer   │ Clause Comparator│ T5 Recommender        │   │
│  │  RoBERTa Q&A   │                  │                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Backend Integration Service (bidirectional HTTP)         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE: SQLite/PostgreSQL │ Prometheus │ Grafana │     │
│                  Docker Compose                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow

1. **Upload** — User uploads document via the Next.js frontend
2. **Store** — Next.js creates `Document` + `Analysis` records in the database
3. **Trigger** — Next.js sends document text to FastAPI (`POST /api/document/analyze`)
4. **Process** — FastAPI runs 7 ML models sequentially with progress callbacks
5. **Deliver** — FastAPI sends results back to Next.js (`POST /api/analysis/results`)
6. **Display** — Dashboard polls for updates and renders the analysis

---

## 🧠 Machine Learning Pipeline

### Model Overview

| # | Model | Base Architecture | Task | Key Metric | Score |
|---|-------|-------------------|------|------------|-------|
| 1 | **LegalBERT NER** | BERT-base | Named Entity Recognition (29 types) | F1 Score | **90.4%** |
| 2 | **CUAD Classifier** | BERT-base | Clause Classification (41 types) | Accuracy | **77.59%** |
| 3 | **BART Summarizer** | BART-large | Abstractive Summarization | ROUGE-1 | **56.81%** |
| 4 | **Risk Scorer** | LegalBERT | Risk Assessment (0–1 scale) | Accuracy | **84.16%** |
| 5 | **Clause Comparator** | Sentence-BERT | Semantic Similarity | MAE | **0.24** |
| 6 | **T5 Recommender** | T5-base | Clause Improvement Generation | ROUGE-1 | **99.88%** |
| 7 | **RoBERTa Q&A** | RoBERTa-base | Extractive Question Answering | Exact Match | **87.18%** |

### Training Datasets

| Model | Dataset | Size | Source |
|-------|---------|------|--------|
| NER | InLegalNER | 10K+ docs | Academic research (Indian legal) |
| Classification | CUAD | 510 contracts, 13K+ annotations | Atticus Project |
| Summarization | BillSum + Custom | 28K docs | Congressional bills + contracts |
| Risk Scoring | Custom Legal Risk | 8K clauses | Expert annotation (3 annotators) |
| Comparison | Legal Clause Pairs | 50K pairs | Contract database |
| Recommendations | Clause Improvements | 15K pairs | Attorney-reviewed |
| Q&A | Legal Q&A Custom | 12K pairs | Contract analysis |

### Model Checkpoints

All trained model weights are stored in `services/legal-ml/checkpoints/`:

```
checkpoints/
├── legalbert/                  # NER model
├── legalbert_cuad_classifier/  # Clause classifier
├── bart_billsum_finetuned/     # Summarization
├── legalbert_risk_scorer/      # Risk scoring
├── legal_comparison_model/     # Clause comparison
├── t5_recommendations/         # Recommendations
└── legalbert_qa/               # Question answering
```

> 📖 For detailed per-model performance metrics, training details, and example outputs, see [`docs/MODEL_PERFORMANCE.md`](docs/MODEL_PERFORMANCE.md)

---

## 🛠️ Tech Stack

### Frontend & Backend
| Technology | Purpose |
|---|---|
| **Next.js 14** | Full-stack React framework (App Router) |
| **TypeScript** | Type-safe development |
| **Tailwind CSS** | Utility-first styling |
| **Radix UI** | Accessible, headless UI components |
| **Framer Motion** | Animations and transitions |
| **Recharts** | Data visualization |
| **React Hook Form + Zod** | Form handling and validation |
| **Prisma ORM** | Database access layer |

### ML Service
| Technology | Purpose |
|---|---|
| **FastAPI** | High-performance Python API framework |
| **PyTorch** | Deep learning framework |
| **Hugging Face Transformers** | Pre-trained model loading and inference |
| **Sentence-Transformers** | Semantic similarity models |
| **spaCy** | NLP preprocessing |
| **scikit-learn** | ML utilities |

### Infrastructure
| Technology | Purpose |
|---|---|
| **Docker + Docker Compose** | Containerized deployment |
| **SQLite / PostgreSQL** | Relational database (Prisma) |
| **Prometheus** | Metrics collection |
| **Grafana** | Monitoring dashboards |

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ and npm
- **Python** 3.11+
- **8GB+ RAM** (ML models require ~6GB)
- **~5GB disk space** for the trimmed inference checkpoints

### 1. Clone the Repository

```bash
git clone https://github.com/ronbell1/nyay-samiti.git
cd nyay-samiti
```

### 2. Set Up the Next.js Application

```bash
# Install dependencies
npm install

# Copy environment config
cp .env.example .env
# Edit .env with your database URL and ML service URL

# Generate Prisma client and push schema
npx prisma generate
npx prisma db push

# Start development server
npm run dev
# → http://localhost:3000
```

### 3. Set Up the ML Service

```bash
# Navigate to ML directory
cd "services/legal-ml"

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
# Edit .env with backend URL

# Start FastAPI server
python main.py
# → http://localhost:8000
# → API docs at http://localhost:8000/docs
```

### 4. (Optional) Docker Deployment

```bash
# Start all services (Next.js, ML service, Prometheus, Grafana)
docker compose up -d
```

---

## 📁 Project Structure

```
nyay-samiti/
├── src/                              # Next.js application
│   ├── app/                          # App Router pages & API routes
│   │   ├── page.tsx                  # Landing page
│   │   ├── layout.tsx                # Root layout (Inter + Playfair Display fonts)
│   │   ├── globals.css               # Global styles
│   │   ├── upload/                   # Document upload page
│   │   ├── dashboard/                # Analysis dashboard
│   │   ├── how-it-works/             # Information page
│   │   ├── contact/                  # Contact page
│   │   ├── sign-in/                  # Authentication
│   │   └── api/                      # Next.js API routes
│   │       ├── documents/            # Document CRUD endpoints
│   │       ├── analysis/             # Analysis management endpoints
│   │       ├── webhooks/             # Webhook handlers
│   │       ├── metrics/              # Prometheus metrics
│   │       └── notify/               # Notification endpoints
│   ├── components/                   # React components
│   │   ├── ui/                       # Radix-based UI primitives
│   │   └── layout/                   # Header, Footer, FloatingChat
│   ├── hooks/                        # Custom React hooks
│   └── lib/                          # Utilities
│       ├── prisma.ts                 # Prisma client singleton
│       ├── ml-service.ts             # ML service HTTP client
│       ├── metrics.ts                # Prometheus metrics
│       └── utils.ts                  # General utilities
│
├── services/legal-ml/                # FastAPI ML microservice
│   ├── main.py                       # FastAPI entry point (7 model routers)
│   ├── app/
│   │   ├── api/                      # API route handlers
│   │   │   ├── routes_ner.py         # NER endpoints
│   │   │   ├── routes_classification.py
│   │   │   ├── routes_risk.py
│   │   │   ├── routes_summary.py
│   │   │   ├── routes_comparison.py
│   │   │   ├── routes_recommendations.py
│   │   │   ├── routes_qa.py
│   │   │   ├── routes_document_analysis.py   # Comprehensive analysis
│   │   │   ├── routes_backend_integration.py # Next.js ↔ FastAPI glue
│   │   │   └── routes_analysis_trigger.py    # Analysis trigger endpoint
│   │   ├── core/                     # Logging, config
│   │   ├── models/                   # Pydantic request/response schemas
│   │   ├── services/                 # ML model service classes
│   │   │   ├── ner/                  # Named Entity Recognition
│   │   │   ├── classification/       # Clause Classification
│   │   │   ├── summarization/        # Document Summarization
│   │   │   ├── risk/                 # Risk Scoring
│   │   │   ├── comparison/           # Clause Comparison
│   │   │   ├── recommendations/      # Clause Improvements
│   │   │   ├── qa/                   # Question Answering
│   │   │   └── backend_integration.py
│   │   └── data/                     # Data utilities
│   ├── checkpoints/                  # Trained inference weights (~5GB)
│   ├── configs/                      # Label schemas, policies
│   ├── model_development/
│   │   ├── datasets/                 # Dataset preparation scripts
│   │   └── training/                 # Model training scripts
│   ├── tests/
│   │   ├── integration/              # 7 integration test suites
│   │   └── unit/                     # Unit tests
│   └── requirements.txt              # Python dependencies
│
├── prisma/
│   └── schema.prisma                 # Database schema (Document, Analysis)
├── examples/sample-documents/        # 7 sample legal documents for testing
├── docs/                             # Documentation
│   ├── MODEL_PERFORMANCE.md          # Detailed model metrics
│   └── WORKFLOW.md                   # End-to-end workflow docs
├── infra/prometheus/                  # Prometheus configuration
├── docker-compose.yml                # Multi-service Docker config
├── Dockerfile                        # Next.js container (multi-stage build)
└── package.json                      # Node.js dependencies
```

---

## 📡 API Reference

### Next.js Backend API (Port 3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents/upload` | Upload a document for analysis |
| `GET` | `/api/documents/[id]` | Get document details |
| `GET` | `/api/analysis/list` | List all analyses |
| `GET/PATCH` | `/api/analysis/[id]/status` | Get/update analysis status |
| `POST` | `/api/analysis/results` | Receive ML analysis results |
| `GET` | `/api/metrics` | Prometheus metrics endpoint |

### FastAPI ML Service (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ner/extract` | Extract named entities |
| `POST` | `/api/classification/classify` | Classify clause types |
| `POST` | `/api/risk/score` | Score contract risk |
| `POST` | `/api/summarize` | Generate document summary |
| `POST` | `/api/compare/*` | Compare clause similarity |
| `POST` | `/api/recommendations/improve` | Get clause improvements |
| `POST` | `/api/qa/answer` | Answer legal questions |
| `POST` | `/api/analyze/complete` | **Full document analysis** (all 7 models) |
| `POST` | `/api/analyze/batch` | Batch document processing |
| `POST` | `/api/document/analyze` | Trigger analysis from Next.js |
| `GET` | `/api/integration/health` | Service health check |
| `GET` | `/health` | Basic health check |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |

### Usage Examples

**Full Document Analysis:**
```bash
curl -X POST "http://localhost:8000/api/analyze/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This Agreement is entered into on January 1, 2025...",
    "document_id": "contract_001",
    "questions": ["What is the governing law?"],
    "summary_length": 150
  }'
```

**Named Entity Extraction:**
```bash
curl -X POST "http://localhost:8000/api/ner/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "This Agreement is between ABC Corp and XYZ Ltd."}'
```

**Risk Assessment:**
```bash
curl -X POST "http://localhost:8000/api/risk/score" \
  -H "Content-Type: application/json" \
  -d '{"text": "The party shall have unlimited liability for any damages."}'
```

---

## 🐳 Docker Deployment

The `docker-compose.yml` orchestrates 4 services:

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| **app** | Custom (Dockerfile) | `3000` | Next.js application |
| **ml-service** | Custom (`services/legal-ml/Dockerfile`) | `8000` | FastAPI ML API |
| **prometheus** | `prom/prometheus` | `9090` | Metrics collection |
| **grafana** | `grafana/grafana` | `3001` | Monitoring dashboards |

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f app

# Stop all services
docker compose down
```

---

## 📈 Monitoring & Observability

- **Prometheus** scrapes metrics from the Next.js app (`/api/metrics`) every 5 seconds
- **Grafana** (port `3001`) provides visual dashboards for request latency, throughput, and model performance
- Application metrics are exported via the `prom-client` library

---

## 🧪 Testing

### ML Service Integration Tests

```bash
cd "services/legal-ml"
source .venv/bin/activate
export PYTHONPATH=$(pwd)

# Run individual model tests
python tests/integration/test_ner_integration.py
python tests/integration/test_cuad_integration.py
python tests/integration/test_summarization_integration.py
python tests/integration/test_risk_integration.py
python tests/integration/test_comparison_integration.py
python tests/integration/test_recommendations_integration.py
python tests/integration/test_qa_integration.py

# Run all tests with pytest
pytest tests/integration/ -v
```

### Sample Documents

The `examples/sample-documents/` directory includes 7 test documents:

- `test-employment-contract.txt`
- `test-nda-agreement.txt`
- `test-partnership-agreement.txt`
- `test-real-estate-agreement.txt`
- `test-service-agreement.txt`
- `test-software-license.txt`
- `test-terms-of-service.txt`

---

## ⚙️ Configuration

### Environment Variables

**Next.js (`.env`)**
```env
DATABASE_URL="file:./dev.db"
ML_SERVICE_URL="http://localhost:8000"
ML_API_KEY="your_secret_ml_api_key"
```

**ML Service (`services/legal-ml/.env`)**
```env
BACKEND_URL="http://localhost:3000/api"
BACKEND_API_KEY="your_secret_backend_api_key"
```

### Database

The project uses **Prisma ORM** with two models:

```prisma
model Document {
  id          String     @id @default(cuid())
  name        String
  content     String?
  contentType String     @default("text/plain")
  size        Int
  uploadedAt  DateTime   @default(now())
  analyses    Analysis[]
}

model Analysis {
  id          String    @id @default(cuid())
  documentId  String
  document    Document  @relation(...)
  status      String    @default("pending")   // pending → processing → completed → failed
  progress    Int       @default(0)
  results     Json?
  error       String?
  startedAt   DateTime  @default(now())
  completedAt DateTime?
}
```

Default: **SQLite** for development. Switch to **PostgreSQL** for production by updating `DATABASE_URL`.

---

## ⚡ Performance Benchmarks

### Processing Time (5–10 page document)

| Model | CPU | GPU | Speedup |
|-------|-----|-----|---------|
| NER | 3.2s | 0.6s | 5.3× |
| Classification | 4.5s | 0.8s | 5.6× |
| Summarization | 8.3s | 1.2s | 6.9× |
| Risk Assessment | 2.1s | 0.4s | 5.2× |
| Comparison | 0.3s | 0.05s | 6.0× |
| Recommendations | 3.8s | 0.7s | 5.4× |
| Q&A (per question) | 1.5s | 0.3s | 5.0× |
| **Total** | **~15s** | **~3s** | — |

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| CPU | 4 cores | 8+ cores |
| GPU | Optional | NVIDIA T4+ |
| Disk | 5 GB | 10 GB |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`docs/MODEL_PERFORMANCE.md`](docs/MODEL_PERFORMANCE.md) | Detailed accuracy, training info, and example outputs for all 7 models |
| [`docs/WORKFLOW.md`](docs/WORKFLOW.md) | End-to-end system workflow with sequence diagrams |
| [`services/legal-ml/README.md`](services/legal-ml/README.md) | ML service setup, API usage, and training instructions |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Frontend
npm run dev          # Next.js dev server (port 3000)
npm run lint         # ESLint

# ML Service
cd "services/legal-ml"
uvicorn main:app --reload   # FastAPI dev server (port 8000)
pytest tests/ -v             # Run tests
```

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright © 2025 [ronbell1](https://github.com/ronbell1), [xpushkal](https://github.com/xpushkal), [justmeetpatel](https://github.com/justmeetpatel)

---

## 🙏 Acknowledgments

- **[CUAD Dataset](https://www.atticusprojectai.org/cuad)** — Contract Understanding Atticus Dataset (510 contracts, 13K+ annotations)
- **[InLegalNER](https://github.com/Legal-NLP-EkStep/InLegalNER)** — Indian Legal Named Entity Recognition Dataset
- **[LegalBERT](https://huggingface.co/nlpaueb/legal-bert-base-uncased)** — Pre-trained legal domain language model
- **[BillSum](https://github.com/FiscalNote/BillSum)** — U.S. Congressional bill summarization dataset
- **[Hugging Face Transformers](https://huggingface.co/transformers/)** — Model training and inference library
- **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance Python web framework

---


**Built with ❤️ for the legal tech community**

⭐ Star this repo if you find it useful!
