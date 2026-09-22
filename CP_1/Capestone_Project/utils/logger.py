"""
logger.py
---------
Centralized logger. Every module does:
    from utils.logger import get_logger
    log = get_logger(__name__)

Logs go to console AND to logs/framework.log (rotated per run isn't
strictly necessary for a capstone, so we keep it simple: one file,
appended, with timestamps).
"""

import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "framework.log"

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "framework") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        # Already configured (avoids duplicate handlers on repeated imports)
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(_FORMAT, datefmt=_DATEFMT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
