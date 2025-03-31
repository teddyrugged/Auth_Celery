from functools import wraps

def count_calls(func):
    """
    Decorator that counts how many times the decorated function was called.
    Prints the count each time the function is executed.
    """
    call_count = 0
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"Function '{func.__name__}' has been called {call_count} times")
        return func(*args, **kwargs)
    
    return wrapper

# Example usage:
if __name__ == "__main__":
    @count_calls
    def example_function():
        print("Hello from example_function")
    
    @count_calls
    def another_function():
        print("Hello from another_function")
    
    example_function()
    example_function()
    another_function()
    example_function()