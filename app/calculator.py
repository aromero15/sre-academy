# calculator.py

def add(x, y):
    """Add two numbers."""
    return x + y

def divide(x, y):
    """Divide x by y. Raises ValueError on division by zero."""
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y
