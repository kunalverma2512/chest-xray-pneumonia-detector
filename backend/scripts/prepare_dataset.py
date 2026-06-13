#!/usr/bin/env python3
"""
backend/scripts/prepare_dataset.py

Downloads the Kaggle chest-xray-pneumonia dataset and organises it into
the directory structure that training.py expects:

  data/processed/
    train/
      NORMAL/
      PNEUMONIA/
    val/
      NORMAL/
      PNEUMONIA/
    test/
      NORMAL/
      PNEUMONIA/

Usage (from the project root):
  # 1. Make sure Kaggle credentials are set up (see note below)
  # 2. Run:
  python backend/scripts/prepare_dataset.py

Kaggle credentials:
  - Create a Kaggle API token at https://www.kaggle.com/account
  - Place kaggle.json at ~/.kaggle/kaggle.json  (chmod 600)
  - OR set env vars: KAGGLE_USERNAME and KAGGLE_KEY

If you have already downloaded the dataset manually:
  - Unzip it so that you have:
      data/raw/chest-xray-pneumonia/chest_xray/{train,val,test}/{NORMAL,PNEUMONIA}
  - Then re-run this script; it will skip the download and only reorganise files.
"""

from __future__ import annotations

import logging
import os
import random
import shutil
import sys
import zipfile
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
KAGGLE_DATASET = "paultimothymooney/chest-xray-pneumonia"
ZIP_NAME = "chest-xray-pneumonia.zip"


def download_dataset() -> Path:
    """Download via Kaggle CLI. Returns the extraction directory."""
    try:
        import kaggle  # noqa: F401 – just checking it's importable
    except ImportError:
        logger.error(
            "kaggle package not found. Install it: pip install kaggle\n"
            "Then set up your API token as described in the script header."
        )
        sys.exit(1)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = RAW_DIR / ZIP_NAME

    if not zip_path.exists():
        logger.info("Downloading %s from Kaggle…", KAGGLE_DATASET)
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "kaggle", "datasets", "download",
             "-d", KAGGLE_DATASET, "-p", str(RAW_DIR)],
            check=False,
        )
        if result.returncode != 0:
            logger.error("Kaggle download failed. See error above.")
            sys.exit(1)
        logger.info("Download complete.")
    else:
        logger.info("Zip already exists – skipping download: %s", zip_path)

    # The zip contents might be in 'chest_xray' or other folders directly in RAW_DIR
    if not (RAW_DIR / "chest_xray").exists() and not (RAW_DIR / "chest-xray-pneumonia").exists():
        logger.info("Extracting %s…", zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(RAW_DIR)
        logger.info("Extraction complete.")
    return RAW_DIR


def find_source_root(base: Path) -> Path:
    """
    Find the chest_xray source directory inside the extracted zip.
    Handles varying archive structures.
    """
    # Typical structure: base/chest_xray/{train,val,test}
    for candidate in [
        base / "chest_xray",
        base,
        base / "chest-xray-pneumonia" / "chest_xray",
    ]:
        if (candidate / "train").exists():
            return candidate
    # Search recursively
    for d in sorted(base.rglob("train")):
        if d.is_dir() and (d.parent / "test").exists():
            return d.parent
    raise FileNotFoundError(
        f"Could not find train/val/test structure inside {base}. "
        "Please check the downloaded archive."
    )


def copy_split(src_split: Path, dst_split: Path) -> dict:
    """Copy all images from src_split/{NORMAL,PNEUMONIA} to dst_split/{NORMAL,PNEUMONIA}."""
    dst_split.mkdir(parents=True, exist_ok=True)
    counts = {}
    for cls in ("NORMAL", "PNEUMONIA"):
        src_cls = src_split / cls
        dst_cls = dst_split / cls
        dst_cls.mkdir(parents=True, exist_ok=True)

        if not src_cls.exists():
            logger.warning("Source class dir not found: %s", src_cls)
            counts[cls] = 0
            continue

        existing = {f.name for f in dst_cls.iterdir() if f.is_file()}
        n = 0
        for img in src_cls.iterdir():
            if img.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            if img.name not in existing:
                shutil.copy2(img, dst_cls / img.name)
            n += 1
        counts[cls] = n
    return counts


def fix_val_split(source_root: Path) -> None:
    """
    The Kaggle chest-xray-pneumonia dataset has a very small val split (only 16 images).
    We expand it by moving 10% of training images to val.
    This only runs if val has fewer than 100 total images.
    """
    val_normal = PROCESSED_DIR / "val" / "NORMAL"
    val_pneumonia = PROCESSED_DIR / "val" / "PNEUMONIA"
    total_val = sum(
        len(list(d.iterdir())) for d in [val_normal, val_pneumonia] if d.exists()
    )
    if total_val >= 100:
        logger.info("Val split has %d images – no expansion needed.", total_val)
        return

    logger.warning(
        "Val split has only %d images. Expanding from training set (10%%)…",
        total_val,
    )
    random.seed(42)
    for cls in ("NORMAL", "PNEUMONIA"):
        train_cls = PROCESSED_DIR / "train" / cls
        val_cls = PROCESSED_DIR / "val" / cls
        val_cls.mkdir(parents=True, exist_ok=True)

        train_images = sorted(train_cls.glob("*.jp*")) + sorted(train_cls.glob("*.png"))
        n_move = max(1, int(len(train_images) * 0.10))
        to_move = random.sample(train_images, n_move)
        for f in to_move:
            shutil.move(str(f), val_cls / f.name)
        logger.info(
            "  Moved %d %s images from train→val", n_move, cls
        )


def print_counts() -> None:
    """Print image counts for all splits and classes."""
    print("\n" + "=" * 55)
    print("  DATASET SUMMARY")
    print("=" * 55)
    total = 0
    for split in ("train", "val", "test"):
        split_dir = PROCESSED_DIR / split
        for cls in ("NORMAL", "PNEUMONIA"):
            cls_dir = split_dir / cls
            n = len(list(cls_dir.glob("*"))) if cls_dir.exists() else 0
            total += n
            print(f"  {split:5s} / {cls:10s}  →  {n:5d} images")
    print("-" * 55)
    print(f"  Total                        →  {total:5d} images")
    print("=" * 55 + "\n")


def main() -> None:
    logger.info("Project root: %s", PROJECT_ROOT)

    # ── Check if data already prepared ──────────────────────────────────────
    train_counts = {
        cls: len(list((PROCESSED_DIR / "train" / cls).glob("*")))
        for cls in ("NORMAL", "PNEUMONIA")
        if (PROCESSED_DIR / "train" / cls).exists()
    }
    if sum(train_counts.values()) > 100:
        logger.info(
            "Processed data already present (train: %s). Skipping download.",
            train_counts,
        )
        fix_val_split(None)
        print_counts()
        return

    # ── Download from Kaggle ─────────────────────────────────────────────────
    extract_dir = download_dataset()
    source_root = find_source_root(extract_dir)
    logger.info("Source dataset root: %s", source_root)

    # ── Copy to processed/ ───────────────────────────────────────────────────
    for split in ("train", "val", "test"):
        src = source_root / split
        dst = PROCESSED_DIR / split
        if not src.exists():
            logger.warning("Source split not found: %s", src)
            continue
        counts = copy_split(src, dst)
        logger.info("Copied split='%s' | counts=%s", split, counts)

    # ── Fix tiny val split ───────────────────────────────────────────────────
    fix_val_split(source_root)

    print_counts()
    logger.info("✅ Dataset preparation complete. Ready for training.")


if __name__ == "__main__":
    main()
