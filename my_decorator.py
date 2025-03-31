# my_decorator.py
from functools import wraps
from typing import Callable, Dict

# Dictionary to store call counts
_call_counts: Dict[str, int] = {}

def count_calls(func: Callable) -> Callable:
    """
    Decorator to count and print how many times a function is called.
    Each function is counted separately.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__
        _call_counts[name] = _call_counts.get(name, 0) + 1
        print(f"{name} has been called {_call_counts[name]} times")
        return func(*args, **kwargs)

    return wrapper


# Example usage
if __name__ == "__main__":

    @count_calls
    def greet(name):
        print(f"Hello, {name}!")

    @count_calls
    def add(x, y):
        return x + y

    greet("Alice")
    greet("Bob")
    greet("Charlie")
    print(add(2, 3))
    print(add(5, 7))
