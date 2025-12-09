import re
import uuid
import logging
from urllib.parse import urlparse

from fastapi import HTTPException
from PIL import Image
from io import BytesIO

# ---------------------------------------------------
# Logger Setup
# ---------------------------------------------------
logger = logging.getLogger("agromind")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# ---------------------------------------------------
# URL Validation
# ---------------------------------------------------
def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except:
        return False


def validate_url_or_throw(url: str):
    if not is_valid_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL provided")


# ---------------------------------------------------
# Image Validation
# ---------------------------------------------------
def validate_image_bytes(image_bytes: bytes):
    """
    Verifies uploaded bytes represent a valid image.
    Prevents corrupted files from reaching your ML model.
    """
    try:
        Image.open(BytesIO(image_bytes))
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")


# ---------------------------------------------------
# Filename / Identifiers
# ---------------------------------------------------
def generate_safe_filename(extension: str = "jpg") -> str:
    return f"{uuid.uuid4().hex}.{extension}"


def generate_uuid() -> str:
    return uuid.uuid4().hex


# ---------------------------------------------------
# Basic Response Formatting
# ---------------------------------------------------
def success(message: str, **data):
    """
    Consistent response shape across all endpoints.
    """
    return {"status": "success", "message": message, "data": data}


def error(message: str):
    raise HTTPException(status_code=400, detail=message)


# ---------------------------------------------------
# Sanity Checks for Crop Model Inputs
# ---------------------------------------------------
def validate_crop_inputs(temperature: float, humidity: float, rainfall: float):
    """
    Ensures values are within realistic Indian agricultural ranges.
    Prevents garbage input from breaking your ML model.
    """
    if not (0 <= temperature <= 60):
        raise HTTPException(status_code=400, detail="Temperature out of valid range (0–60°C)")

    if not (0 <= humidity <= 100):
        raise HTTPException(status_code=400, detail="Humidity out of valid range (0–100%)")

    if not (0 <= rainfall <= 1000):
        raise HTTPException(status_code=400, detail="Rainfall must be between 0–1000 mm")


# ---------------------------------------------------
# Log Helper
# ---------------------------------------------------
def log_event(event: str, **meta):
    """
    Unified logging for all events: predictions, feedback, errors, etc.
    """
    logger.info(f"{event} | {meta}")
