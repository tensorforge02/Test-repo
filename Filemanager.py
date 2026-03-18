# file_manager.py - Safe file handling utilities

import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".txt", ".json", ".csv", ".log"}
MAX_FILE_SIZE_MB = 10


def is_safe_path(base_dir: str, filepath: str) -> bool:
    """Check that filepath stays within base_dir (prevents path traversal)."""
    base = os.path.realpath(base_dir)
    target = os.path.realpath(filepath)
    return target.startswith(base)


def read_file(base_dir: str, filename: str) -> Optional[str]:
    """
    Safely read a file within base_dir.

    Validates path traversal, extension, and file size before reading.
    """
    filepath = os.path.join(base_dir, filename)

    if not is_safe_path(base_dir, filepath):
        logger.error("Path traversal attempt blocked: %s", filename)
        return None

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.error("Disallowed file extension: %s", ext)
        return None

    try:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            logger.error("File too large (%.1f MB): %s", size_mb, filename)
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("File not found: %s", filepath)
        return None
    except PermissionError:
        logger.error("Permission denied: %s", filepath)
        return None


def write_file(base_dir: str, filename: str, content: str) -> bool:
    """Safely write content to a file within base_dir."""
    filepath = os.path.join(base_dir, filename)

    if not is_safe_path(base_dir, filepath):
        logger.error("Path traversal attempt blocked: %s", filename)
        return False

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.error("Disallowed file extension: %s", ext)
        return False

    try:
        os.makedirs(base_dir, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError as e:
        logger.error("Error writing file %s: %s", filepath, e)
        return False


def read_json(base_dir: str, filename: str) -> Optional[dict]:
    """Read and parse a JSON file safely."""
    content = read_file(base_dir, filename)
    if content is None:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", filename, e)
        return None


def delete_file(base_dir: str, filename: str) -> bool:
    """Safely delete a file within base_dir."""
    filepath = os.path.join(base_dir, filename)

    if not is_safe_path(base_dir, filepath):
        logger.error("Path traversal attempt blocked: %s", filename)
        return False

    try:
        os.remove(filepath)
        return True
    except FileNotFoundError:
        logger.warning("File already gone: %s", filepath)
        return False
    except OSError as e:
        logger.error("Error deleting %s: %s", filepath, e)
        return False