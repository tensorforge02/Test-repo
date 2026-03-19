# calculator.py - Basic calculator module

def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float | None:
    """Return a divided by b, or None if b is zero."""
    if b == 0:
        return None
    return a / b


def power(base: float, exp: int) -> float:
    """Return base raised to the power of exp."""
    return base ** exp


def percentage(value: float, total: float) -> float | None:
    """Return what percentage value is of total."""
    if total == 0:
        return None
    return (value / total) * 100