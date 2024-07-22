from functools import wraps


def check_zero_division(function):
    """Checks if operation is division by zero, prints a message if it is.

    Decorated function should take 2 numeric arguments: dividend and divisor.
    """
    @wraps(function)
    def wrapper(a, b):
        if b == 0:
            print('Division by zero detected.')
        else:
            return function(a, b)

    return wrapper


def print_arguments(function):
    """Prints the arguments of the decorated function."""
    @wraps(function)
    def wrapper(*args):
        print(f'Arguments of function {function.__name__}: {args}')
        return function(*args)

    return wrapper
