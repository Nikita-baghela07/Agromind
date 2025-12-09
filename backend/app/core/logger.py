import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agromind.log"

logger = logging.getLogger("agromind")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

# Avoid adding handlers multiple times (useful with reloads)
if not logger.handlers:
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    # Rotating file handler
    fh = RotatingFileHandler(
        filename=str(LOG_FILE),
        maxBytes=2 * 1024 * 1024,  # 2MB
        backupCount=5,
        encoding="utf-8",
    )
    fh.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)


def log_event(event: str, **meta):
    """
    Helper to log structured events.
    """
    if meta:
        logger.info(f"{event} | {meta}")
    else:
        logger.info(event)
