# PneumoDetectAI – Project Makefile
# Run all commands from the project root

VENV     = backend/.venv
PYTHON   = $(VENV)/bin/python
PIP      = $(VENV)/bin/pip
UVICORN  = $(VENV)/bin/uvicorn

.PHONY: help setup install download-data prepare-data train evaluate start-backend start-frontend dev

help:
	@echo ""
	@echo "  PneumoDetectAI – Available commands"
	@echo "  ======================================"
	@echo "  make setup           Create Python 3.11 venv and install all dependencies"
	@echo "  make download-data   Set up Kaggle credentials and download dataset"
	@echo "  make prepare-data    Organise raw dataset into train/val/test splits"
	@echo "  make train           Train the MobileNetV2 model (runs ~10-20 min)"
	@echo "  make evaluate        Run internal test-set evaluation"
	@echo "  make start-backend   Start the FastAPI backend at localhost:8000"
	@echo "  make start-frontend  Start the Vite dev server at localhost:5173"
	@echo "  make dev             Start both backend and frontend (requires two terminals)"
	@echo ""

# ─── SETUP ──────────────────────────────────────────────────────────────────

setup:
	@echo "→ Creating Python 3.11 virtual environment…"
	python3.11 -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r backend/requirements.txt
	@echo "→ Installing frontend dependencies…"
	cd frontend && npm install
	@echo "✅ Setup complete!"

# ─── DATASET ────────────────────────────────────────────────────────────────

download-data:
	@echo "→ Downloading chest X-ray dataset from Kaggle…"
	$(PYTHON) backend/scripts/download_dataset.py

setup-kaggle:
	@echo "→ Setting up Kaggle API credentials…"
	$(PYTHON) backend/scripts/download_dataset.py --setup-kaggle

prepare-data:
	@echo "→ Organising dataset into train/val/test splits…"
	$(PYTHON) backend/scripts/prepare_dataset.py

# ─── ML PIPELINE ────────────────────────────────────────────────────────────

train:
	@echo "→ Starting model training (this will take 10-20 minutes)…"
	$(PYTHON) backend/scripts/run_training.py --epochs 25 --batch-size 32

train-fast:
	@echo "→ Quick training run (5 epochs for testing)…"
	$(PYTHON) backend/scripts/run_training.py --epochs 5 --batch-size 32

evaluate:
	@echo "→ Running internal evaluation…"
	$(PYTHON) backend/scripts/run_evaluation.py

# ─── SERVERS ────────────────────────────────────────────────────────────────

start-backend:
	@echo "→ Starting FastAPI backend at http://localhost:8000"
	@echo "   API docs: http://localhost:8000/docs"
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --app-dir backend --reload

start-frontend:
	@echo "→ Starting Vite frontend at http://localhost:5173"
	cd frontend && npm run dev

# ─── MISC ────────────────────────────────────────────────────────────────────

clean-data:
	@echo "→ Removing processed data (keeps raw downloads)"
	rm -rf data/processed/train data/processed/val data/processed/test

clean-model:
	@echo "→ Removing trained model files"
	rm -f models/*.h5 models/*.png
