# Fraud Detection System

A multi-agent fraud detection system using LangGraph and various ML models.

## Features

- Data ingestion and validation
- Feature engineering
- Rule-based detection
- Anomaly detection
- Graph-based analysis
- Risk scoring
- Decision making with explainability
- Learning and feedback loops
- REST API
- Interactive dashboard

## Project Structure

```
fraud_detection_system/
├── agents/           # Agent implementations
├── orchestration/    # LangGraph pipeline
├── models/          # ML models
├── api/             # FastAPI endpoints
├── dashboard/       # Streamlit dashboard
├── data/            # Data files
├── core/            # Core utilities
├── tests/           # Test suite
└── notebooks/       # Analysis notebooks
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the system:
```bash
python app.py
```

## API Usage

Start the API server:
```bash
uvicorn api.main:app --reload
```

## Dashboard

Start the Streamlit dashboard:
```bash
streamlit run dashboard/app.py
```

## Testing

Run tests:
```bash
pytest
```

## Documentation

See individual README files in each module for detailed documentation.
