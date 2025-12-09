import os
import uuid
from typing import Optional
from fastapi import UploadFile
from pathlib import Path

# Base directory for all uploaded files (configure anytime)
UPLOAD_DIR = Path("app/static/uploads")

# Ensure directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_file(file: UploadFile, subfolder: str = "") -> str:
    """
    Saves an uploaded file inside static/uploads.
    
    Args:
        file (UploadFile): File uploaded by user
        subfolder (str): Optional subfolder (ex: "diseases", "feedback")

    Returns:
        str: relative path to the saved file
    """
    folder = UPLOAD_DIR / subfolder
    folder.mkdir(parents=True, exist_ok=True)

    # Unique filename
    extension = file.filename.split(".")[-1]
    new_filename = f"{uuid.uuid4().hex}.{extension}"

    filepath = folder / new_filename

    # Save file content
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return str(filepath)


def save_bytes(content: bytes, subfolder: str = "", extension: str = "jpg") -> str:
    """
    Save raw bytes as file. Useful when downloading image from URL.
    """
    folder = UPLOAD_DIR / subfolder
    folder.mkdir(parents=True, exist_ok=True)

    new_filename = f"{uuid.uuid4().hex}.{extension}"
    filepath = folder / new_filename

    with open(filepath, "wb") as buffer:
        buffer.write(content)

    return str(filepath)


def read_file(path: str) -> Optional[bytes]:
    """
    Reads a file from disk and returns its bytes.
    """
    path = Path(path)
    if not path.exists():
        return None
    return path.read_bytes()


def delete_file(path: str) -> bool:
    """
    Deletes a file safely.
    Returns:
        True if deleted, False if not found.
    """
    path_obj = Path(path)
    if path_obj.exists():
        path_obj.unlink()
        return True
    return False
