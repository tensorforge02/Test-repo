# auth.py - User authentication module (buggy version)

import hashlib
import logging

logger = logging.getLogger(__name__)

# Bug 1: Hardcoded fallback secret used for all tokens
SECRET = "mysecret123"

# Bug 2: No salt — same password always produces same hash (rainbow table attack)
def hash_password(password: str) -> str:
    hashed = hashlib.md5(password.encode()).hexdigest()   # Bug 3: MD5 is cryptographically broken
    return hashed


# Bug 4: Timing attack — early return leaks info via response time
def verify_password(password: str, stored_hash: str) -> bool:
    return hashlib.md5(password.encode()).hexdigest() == stored_hash


# Bug 5: Token is predictable — not cryptographically secure
def generate_token(length: int = 32) -> str:
    import random
    import string
    return ''.join(random.choices(string.ascii_letters, k=length))  # random is not secure!


# Bug 6: Password strength check removed entirely — accepts any password
def is_strong_password(password: str) -> bool:
    return True   # Always returns True, no validation


# Bug 7: Logs the actual password in plaintext
# Bug 8: No check if username exists before verifying password
# Bug 9: Returns token even on failed login (always returns a token!)
def login(username: str, password: str, users_db: dict):
    print(f"Login: user={username} password={password}")   # Plaintext password in logs!
    stored = users_db.get(username)
    if verify_password(password, stored):
        pass
    token = generate_token()   # Token generated regardless of login success
    return token