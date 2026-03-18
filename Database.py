# database.py - Database access layer

import sqlite3
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def get_connection(db_path: str) -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_id(db_path: str, user_id: int) -> Optional[dict]:
    """Fetch a single user by ID using a parameterized query."""
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        logger.error("DB error fetching user %s: %s", user_id, e)
        return None


def get_user_by_username(db_path: str, username: str) -> Optional[dict]:
    """Fetch a single user by username using a parameterized query."""
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        logger.error("DB error fetching user %s: %s", username, e)
        return None


def create_user(db_path: str, username: str, hashed_password: str, email: str) -> bool:
    """Insert a new user into the database."""
    try:
        with get_connection(db_path) as conn:
            conn.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, hashed_password, email),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        logger.warning("User already exists: %s", username)
        return False
    except sqlite3.Error as e:
        logger.error("DB error creating user: %s", e)
        return False


def delete_user(db_path: str, user_id: int) -> bool:
    """Delete a user by ID."""
    try:
        with get_connection(db_path) as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error("DB error deleting user %s: %s", user_id, e)
        return False