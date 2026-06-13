# PneumoDetectAI

A full-stack clinical AI tool for pneumonia detection from pediatric chest X-rays.  
Upload a chest X-ray → receive a diagnosis, confidence score, and clinical recommendation in under 2 seconds.

---

## Validation Results

Evaluated on **485 independent cross-operator samples** — fully separate from training data.

| Metric | Score |
|---|---|
| Accuracy | **82.7%** |
| Sensitivity (Recall) | **97.6%** |
| Specificity | **66.7%** |
| Precision (PPV) | **75.9%** |
| F1 Score | **0.854** |
| ROC-AUC | **0.961** |
| Internal Accuracy | **94.8%** (held-out test split) |

> Sensitivity is prioritised over specificity by design — in pneumonia screening, missing a true case (false negative) is far more dangerous than triggering an unnecessary follow-up (false positive).

---

## What It Does

1. **Upload** — Drag-and-drop a JPEG or PNG pediatric chest X-ray (≤10 MB) into the web UI
2. **Infer** — The FastAPI backend resizes the image to 224×224, normalises to [0,1], and runs it through the fine-tuned MobileNetV2 model
3. **Report** — The frontend displays diagnosis (PNEUMONIA / NORMAL), raw confidence score, confidence tier (High / Moderate / Low), a clinical recommendation, and cross-operator validation provenance

No images are persisted. All inference happens in-memory.

---

## Architecture

```
frontend/          React 18 + Vite — upload UI, metrics dashboard, result report
backend/
  app/
    api/           FastAPI routes — /predict, /health, /metrics
    ml/            MobileNetV2 model, training pipeline, evaluation scripts
    core/          Config — validated metrics, model settings
    schemas/       Pydantic request/response schemas
    utils/         Image preprocessing helpers
```

**Frontend → Backend communication:** REST (JSON)  
**Model serving:** Uvicorn (ASGI)  
**Inference time:** ~1–2 seconds per image on CPU; faster on GPU

---

## Model

| Detail | Value |
|---|---|
| Architecture | MobileNetV2 (ImageNet pre-trained, fine-tuned) |
| Input | 224 × 224 RGB, normalised to [0, 1] |
| Output | Sigmoid scalar — threshold 0.5 |
| Loss | Binary cross-entropy |
| Optimiser | Adam — lr=0.001 with cosine decay |
| Callbacks | EarlyStopping (patience=7), ReduceLROnPlateau |
| Training device | Apple Silicon (Metal/MPS GPU) |
| Dataset | 5,216 balanced images — 1:1 Normal : Pneumonia |
| Framework | TensorFlow / Keras 2.x |

---

## Tech Stack

| Layer | Technologies |
|---|---|
| ML / AI | TensorFlow, Keras, MobileNetV2, NumPy, scikit-learn |
| Backend | Python 3.11, FastAPI, Uvicorn, Pillow |
| Frontend | React 18, Vite, JavaScript (ES2022), CSS3 |
| Dev Tools | Git, Makefile, Apple Metal (MPS) GPU acceleration |

---

## Setup Guide

### Prerequisites

- Python 3.10 or 3.11
- Node.js 18+
- `make` (optional but recommended)

### 1. Clone the repository

```bash
git clone https://github.com/kunalverma2512/chest-xray-pneumonia-detector.git
cd chest-xray-pneumonia-detector
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up your environment variables:

```bash
cp .env.example .env            # edit if needed
```

Start the API server:

```bash
uvicorn app.main:app --reload --port 8000
```

API is now available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend is now available at `http://localhost:5173` (or `5174` if port is in use).

### 4. Using the Makefile (recommended)

From the project root:

```bash
make install         # install all dependencies (backend + frontend)
make start-backend   # start FastAPI server
make start-frontend  # start Vite dev server
```

---

## Project Structure

```
chest-xray-pneumonia-detector/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # inference.py, health.py
│   │   ├── core/               # config.py (validated metrics, settings)
│   │   ├── ml/                 # model.py, training.py, evaluation.py
│   │   ├── schemas/            # Pydantic models
│   │   └── utils/              # io.py (image helpers)
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/         # Navbar, landing sections, upload UI, metrics
│   │   ├── pages/              # Home, Upload, ModelInsights, About, FAQ, Contact
│   │   ├── layouts/            # MainLayout
│   │   └── utils/              # formatters.js
│   ├── index.html
│   └── vite.config.js
├── data/
│   ├── raw/                    # original Kaggle dataset
│   ├── processed/              # balanced, preprocessed splits
│   └── external/cross_op/      # 485 independent validation samples
├── Makefile
└── README.md
```

---

## Disclaimer

This tool is for **research and preliminary screening purposes only**.  
It has not received FDA, CE, or equivalent regulatory clearance.  
All results must be reviewed by a qualified clinician before any clinical decision.
