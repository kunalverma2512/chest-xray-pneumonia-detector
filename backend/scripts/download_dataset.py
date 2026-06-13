#!/usr/bin/env python3
"""
backend/scripts/download_dataset.py

Downloads the Kaggle chest-xray-pneumonia dataset automatically.

TWO METHODS:
  Method 1 (Kaggle API - recommended):
    1. Get your Kaggle API token at https://www.kaggle.com/settings → Account → Create New Token
    2. This downloads kaggle.json with your username and key
    3. Run:  python backend/scripts/download_dataset.py --setup-kaggle
       (it will prompt for your username and key and save ~/.kaggle/kaggle.json)

  Method 2 (opendatasets - browser auth):
    1. Run:  python backend/scripts/download_dataset.py --browser
    2. It will open a browser to authenticate and download automatically.

  Method 3 (manual):
    1. Go to: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
    2. Download the zip
    3. Extract to:  data/raw/chest-xray-pneumonia/
    4. Run:  python backend/scripts/prepare_dataset.py

Usage (from project root):
  python backend/scripts/download_dataset.py
  python backend/scripts/download_dataset.py --setup-kaggle
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
KAGGLE_DATASET = "paultimothymooney/chest-xray-pneumonia"

VENV_PYTHON = PROJECT_ROOT / "backend" / ".venv" / "bin" / "python"
PYTHON = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def setup_kaggle_credentials() -> None:
    """Interactively set up Kaggle API credentials."""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"

    if kaggle_json.exists():
        logger.info("Kaggle credentials already exist at %s", kaggle_json)
        return

    print("\n" + "=" * 60)
    print("  KAGGLE API SETUP")
    print("=" * 60)
    print("Get your Kaggle API token:")
    print("  1. Go to: https://www.kaggle.com/settings")
    print("  2. Click 'Account' tab → 'Create New API Token'")
    print("  3. Download kaggle.json and enter the credentials below")
    print("=" * 60 + "\n")

    username = input("Enter your Kaggle username: ").strip()
    key = input("Enter your Kaggle API key: ").strip()

    import json
    kaggle_dir.mkdir(exist_ok=True)
    kaggle_json.write_text(json.dumps({"username": username, "key": key}))
    kaggle_json.chmod(0o600)
    logger.info("Kaggle credentials saved to %s", kaggle_json)


def download_via_kaggle_api() -> bool:
    """Download dataset using kaggle CLI."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = RAW_DIR / "chest-xray-pneumonia.zip"

    if zip_path.exists():
        logger.info("Dataset zip already exists: %s", zip_path)
        return True

    logger.info("Downloading %s via Kaggle API…", KAGGLE_DATASET)
    result = subprocess.run(
        [PYTHON, "-m", "kaggle", "datasets", "download",
         "-d", KAGGLE_DATASET, "-p", str(RAW_DIR)],
        check=False
    )
    if result.returncode != 0:
        return False

    # Extract
    import zipfile
    logger.info("Extracting zip…")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(RAW_DIR)
    logger.info("Extraction complete.")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the chest X-ray dataset.")
    parser.add_argument("--setup-kaggle", action="store_true",
                        help="Interactively set up Kaggle API credentials first.")
    args = parser.parse_args()

    if args.setup_kaggle:
        setup_kaggle_credentials()

    # Check if data already present
    processed_dir = PROJECT_ROOT / "data" / "processed" / "train" / "NORMAL"
    if processed_dir.exists() and len(list(processed_dir.glob("*"))) > 100:
        logger.info("✅ Dataset already prepared. Skipping download.")
        subprocess.run([PYTHON, str(PROJECT_ROOT / "backend" / "scripts" / "prepare_dataset.py")])
        return

    # Try Kaggle API
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    access_token = Path.home() / ".kaggle" / "access_token"
    if kaggle_json.exists() or access_token.exists():
        success = download_via_kaggle_api()
        if success:
            # Now run prepare_dataset to organise
            subprocess.run(
                [PYTHON, str(PROJECT_ROOT / "backend" / "scripts" / "prepare_dataset.py")],
                check=True
            )
            logger.info("✅ Dataset downloaded and prepared!")
            return
    else:
        print("\n" + "=" * 65)
        print("  MANUAL DATASET DOWNLOAD REQUIRED")
        print("=" * 65)
        print("\nKaggle credentials not found. Please download manually:\n")
        print("  1. Go to: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia")
        print("  2. Click 'Download' (you need a free Kaggle account)")
        print("  3. Save the zip to:")
        print(f"     {RAW_DIR / 'chest-xray-pneumonia.zip'}")
        print("  4. Then run:")
        print(f"     {PYTHON} backend/scripts/prepare_dataset.py\n")
        print("OR set up Kaggle API credentials:")
        print(f"     {PYTHON} backend/scripts/download_dataset.py --setup-kaggle\n")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
