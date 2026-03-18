# database.py - Database access layer (buggy version)

import sqlite3
import logging

logger = logging.getLogger(__name__)

# Bug 1: Global connection shared across all calls (not thread-safe)
_conn = None

def get_connection(db_path: str) -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(db_path)  # Never closed, shared globally
    return _conn


# Bug 2: SQL Injection — user input directly concatenated into query
def get_user_by_id(db_path: str, user_id):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + str(user_id)  # Injection risk!
    cursor.execute(query)
    return cursor.fetchone()


# Bug 3: SQL Injection via username
# Bug 4: Returns raw tuple instead of dict — breaks callers expecting dict
def get_user_by_username(db_path: str, username: str):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"  # Injection!
    cursor.execute(query)
    return cursor.fetchone()   # Returns tuple, not dict


# Bug 5: Password stored as plaintext
# Bug 6: No error handling — crashes on duplicate user
def create_user(db_path: str, username: str, password: str, email: str):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, password, email),   # Plaintext password saved!
    )
    conn.commit()
    # Bug 7: No return value — caller can't tell if it succeeded


# Bug 8: Deletes by username string but accepts any input — no validation
# Bug 9: No error handling
def delete_user(db_path: str, user_id):
    conn = get_connection(db_path)
    conn.execute("DELETE FROM users WHERE id = " + str(user_id))  # Injection!
    conn.commit()
    return True   # Always returns True even if nothing was deleted