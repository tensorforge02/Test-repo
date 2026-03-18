# auth.py - User authentication module

import hashlib
import secrets
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash a password securely using SHA-256 with a random salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plain password against a stored hash."""
    try:
        salt, hashed = stored_hash.split(":", 1)
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
    except ValueError:
        logger.error("Invalid hash format")
        return False


def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_hex(length)


def is_strong_password(password: str) -> bool:
    """Check if a password meets strength requirements."""
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()" for c in password)
    return has_upper and has_digit and has_special


def login(username: str, password: str, users_db: dict) -> Optional[str]:
    """
    Authenticate a user and return a session token on success.

    Args:
        username: The user's username.
        password: The plain-text password to verify.
        users_db: Dict mapping username -> stored_hash.

    Returns:
        A session token string, or None if authentication fails.
    """
    if username not in users_db:
        logger.warning("Login attempt for unknown user: %s", username)
        return None
    if not verify_password(password, users_db[username]):
        logger.warning("Failed login for user: %s", username)
        return None
    token = generate_token()
    logger.info("Successful login for user: %s", username)
    return token