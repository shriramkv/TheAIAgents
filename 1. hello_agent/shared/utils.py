"""
Utility functions used across the Hello Agent.
"""
import re

def is_math_query(query: str) -> bool:
    """
    Detects if a query involves mathematical operations.
    Returns True if the query contains basic math operators and numbers.
    """
    # Simple heuristic to detect math queries
    math_chars = bool(re.search(r'[\+\-\*\/]\s*\d', query))
    math_words = any(word in query.lower() for word in ['math', 'calculate', 'add', 'multiply', 'subtract', 'divide'])
    # If the user is just giving a raw expression like "25 * 18"
    raw_expr = bool(re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', query))
    return math_chars or math_words or raw_expr

def is_string_query(query: str) -> bool:
    """
    Detects if query involves string operations like reverse.
    """
    return 'reverse' in query.lower()
