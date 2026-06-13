# PneumoDetectAI – Backend

FastAPI backend for the pediatric chest X-ray pneumonia detection AI.

## Quick Start

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Apple Silicon only – for Metal GPU acceleration)
#    Replace `tensorflow` in requirements.txt with:
#    pip install tensorflow-macos tensorflow-metal

# 4. Copy and configure environment
cp .env.example .env
# Edit .env if needed (e.g. MODEL_PATH_OVERRIDE)

# 5. Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive docs: http://localhost:8000/docs

---

## Directory Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI app + lifespan
│   ├── api/
│   │   └── v1/
│   │       ├── router.py          # Aggregates all v1 routers
│   │       └── endpoints/
│   │           ├── health.py      # GET /api/v1/health, /info, /stats
│   │           └── inference.py   # POST /api/v1/predict
│   ├── core/
│   │   ├── config.py              # Pydantic settings (env-driven)
│   │   └── logging.py             # Structured logging setup
│   ├── ml/
│   │   ├── model.py               # Model loader + preprocessing + inference
│   │   ├── training.py            # ChestXRayTrainer (MobileNetV2)
│   │   └── evaluation.py          # ModelEvaluator + CrossOperatorValidator
│   ├── schemas/
│   │   └── inference.py           # Pydantic request/response models
│   └── utils/
│       └── io.py                  # Image I/O helpers
├── scripts/
│   ├── run_training.py            # CLI: train the model
│   ├── run_evaluation.py          # CLI: evaluate on internal test set
│   └── run_cross_operator_validation.py  # CLI: cross-operator validation
├── tests/
│   ├── test_inference.py          # Unit tests (no model needed)
│   └── test_health.py             # Integration tests (TestClient)
├── .env.example                   # Environment variable template
├── pyproject.toml                 # pytest + ruff config
└── requirements.txt               # Python dependencies
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/`  | Root liveness probe |
| `GET`  | `/api/v1/health` | Model readiness check |
| `GET`  | `/api/v1/info`   | Architecture & clinical metadata |
| `GET`  | `/api/v1/stats`  | Cross-operator validation metrics |
| `POST` | `/api/v1/predict` | **Chest X-ray inference** |

### POST /api/v1/predict

**Request**: `multipart/form-data` with a `file` field (JPEG / PNG / WebP, ≤ 10 MB).

**Response**:
```json
{
  "diagnosis": "PNEUMONIA",
  "confidence": 94.3,
  "confidence_level": "High",
  "raw_score": 0.943,
  "recommendation": "Strong indication of pneumonia. Recommend immediate medical attention.",
  "external_validation_performance": {
    "accuracy": "86.0%",
    "sensitivity": "96.4%",
    "specificity": "74.8%",
    "validated_on": "485 independent samples"
  },
  "disclaimer": "This AI assistant is for preliminary screening only. Always consult healthcare professionals for medical decisions.",
  "filename": "chest_xray.jpg",
  "image_size": "1024x768",
  "timestamp": "2026-06-13T21:49:00"
}
```

---

## Model Location

The server searches for the model in this order:

1. `MODEL_PATH_OVERRIDE` env var (explicit path)
2. `../api/streamlit_api_folder/best_chest_xray_model.h5` (existing repo location)
3. `../models/best_chest_xray_model.h5`
4. `models/best_chest_xray_model.h5` (backend-local)

---

## Running Tests

```bash
# From backend/ directory
pytest tests/ -v
```

---

## CLI Scripts

```bash
# Train the model (requires processed data)
python scripts/run_training.py --epochs 25 --batch-size 32

# Evaluate on internal test set
python scripts/run_evaluation.py

# Cross-operator validation
python scripts/run_cross_operator_validation.py \
    --dataset-path /path/to/cross_operator_validation_dataset/test
```

---

## CORS

In development, the API allows requests from `http://localhost:5173` (Vite default).
To add more origins, set the `CORS_ORIGINS` env var in `.env`:

```
CORS_ORIGINS=http://localhost:5173,https://your-app.vercel.app
```
