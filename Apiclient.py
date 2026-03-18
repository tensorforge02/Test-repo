# api_client.py - External API client

import logging
import time
from typing import Optional
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.example.com/v1"
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3


def _make_request(
    method: str,
    endpoint: str,
    api_key: str,
    payload: Optional[dict] = None,
    retries: int = MAX_RETRIES,
) -> Optional[dict]:
    """
    Internal helper to make an authenticated API request with retry logic.

    Args:
        method: HTTP method ('GET', 'POST', etc.)
        endpoint: API endpoint path (e.g. '/users/1')
        api_key: API key sent securely in Authorization header
        payload: Optional JSON body for POST/PUT requests
        retries: Number of retry attempts on transient failures

    Returns:
        Parsed JSON response dict, or None on failure.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{BASE_URL}{endpoint}"

    for attempt in range(1, retries + 1):
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=payload,
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.warning("Timeout on attempt %d for %s", attempt, url)
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error %s: %s", response.status_code, e)
            if response.status_code < 500:
                return None         # Don't retry client errors (4xx)
        except requests.exceptions.RequestException as e:
            logger.error("Request error on attempt %d: %s", attempt, e)

        if attempt < retries:
            time.sleep(2 ** attempt)    # Exponential backoff

    logger.error("All %d attempts failed for %s", retries, url)
    return None


def get_user(user_id: int, api_key: str) -> Optional[dict]:
    """Fetch a user by ID from the API."""
    return _make_request("GET", f"/users/{user_id}", api_key)


def create_order(order_data: dict, api_key: str) -> Optional[dict]:
    """Create a new order via the API."""
    if not order_data.get("user_id") or not order_data.get("items"):
        logger.error("Invalid order data: missing user_id or items")
        return None
    return _make_request("POST", "/orders", api_key, payload=order_data)


def update_profile(user_id: int, profile_data: dict, api_key: str) -> bool:
    """Update a user's profile. Returns True on success."""
    result = _make_request("PUT", f"/users/{user_id}", api_key, payload=profile_data)
    return result is not None