"""
backend/app/core/logging.py

Configures application-wide structured logging.
Call `setup_logging()` once during application startup (in main.py lifespan).
"""

from __future__ import annotations

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Configure root logger with a consistent format.

    Args:
        level:    Logging level string, e.g. "DEBUG", "INFO", "WARNING".
        log_file: Optional path to write logs to a file in addition to stdout.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    fmt = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    for handler in handlers:
        handler.setFormatter(formatter)

    logging.basicConfig(level=numeric_level, handlers=handlers, force=True)

    # Quiet noisy third-party loggers
    for noisy in ("tensorflow", "absl", "PIL", "h5py", "urllib3", "httpx"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Convenience wrapper – use this instead of `logging.getLogger` directly."""
    return logging.getLogger(name)
