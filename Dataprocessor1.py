# data_processor.py - Data processing utilities (buggy version)

import logging

logger = logging.getLogger(__name__)


# Bug 1: Crashes on empty list — no guard
def average(numbers):
    return sum(numbers) / len(numbers)   # ZeroDivisionError if empty!


# Bug 2: O(n²) nested loop instead of O(n) set approach
def find_duplicates(items):
    duplicates = []
    for i in items:
        for j in items:                  # Extremely slow on large lists
            if i == j and i not in duplicates:
                duplicates.append(i)
    return duplicates


# Bug 3: Modifies the input list while iterating — skips elements!
def remove_negatives(numbers):
    for n in numbers:
        if n < 0:
            numbers.remove(n)            # Mutates list during iteration
    return numbers


# Bug 4: No zero check — crashes on b=0
def safe_divide(a, b):
    return a / b                         # ZeroDivisionError!


# Bug 5: Normalize returns wrong results — divides by max only, not range
def normalize(values):
    if not values:
        return []
    max_val = max(values)
    if max_val == 0:
        return values
    return [v / max_val for v in values]  # Wrong formula — not [0,1] normalization


# Bug 6: Chunk size of 0 causes infinite loop
def chunk(items, size):
    result = []
    for i in range(0, len(items), size):  # range(0, n, 0) raises ValueError — no guard
        result.append(items[i : i + size])
    return result


# Bug 7: String concatenation in loop — O(n²) memory usage
def build_report(items):
    report = ""
    for item in items:
        report = report + "- " + item + "\n"   # New string object created each iteration
    return report