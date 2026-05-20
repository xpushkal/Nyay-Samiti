# Tests

This directory contains all tests for the Nyay-Samiti Legal AI project.

## Structure

```
tests/
├── integration/     # Integration tests for ML services
│   ├── test_ner_integration.py
│   ├── test_cuad_integration.py
│   ├── test_summarization_integration.py
│   ├── test_risk_integration.py
│   ├── test_comparison_integration.py
│   ├── test_recommendations_integration.py
│   └── test_qa_integration.py
└── unit/           # Unit tests (to be added)
```

## Running Integration Tests

Each integration test can be run independently:

```bash
# Set PYTHONPATH
export PYTHONPATH=/Users/pushkalpratapsingh/Downloads/nyay-samiti

# Run individual tests
python tests/integration/test_ner_integration.py
python tests/integration/test_cuad_integration.py
python tests/integration/test_summarization_integration.py
python tests/integration/test_risk_integration.py
python tests/integration/test_comparison_integration.py
python tests/integration/test_recommendations_integration.py
python tests/integration/test_qa_integration.py
```

Or use pytest (when installed):

```bash
pytest tests/integration/
```

## Test Coverage

- ✅ NER Model - Named Entity Recognition
- ✅ CUAD Classifier - Clause Classification (41 types)
- ✅ Summarization - Document Summarization
- ✅ Risk Scoring - Risk Assessment (1-10 scale)
- ✅ Comparison - Clause Similarity Detection
- ✅ Recommendations - Clause Improvement Suggestions
- ✅ QA - Legal Question Answering

All models tested with real-world legal text examples.
