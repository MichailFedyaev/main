from functools import wraps
from typing import Any, Callable


def log(filename: Any) -> Callable:
    """Логирует вызов функции и ее результат в файл или на консоль."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} called with args: {args}, kwargs:{kwargs}. Result: {result}"
            except Exception as e:
                log_message = f"{func.__name__} error: {e}. Inputs:{args}, {kwargs}"
                if filename:
                    try:
                        with open(filename, "a", encoding="utf-8") as file:
                            file.write(log_message + "\n")
                    except Exception as e:
                        print(f"Error writing to log file: {e}")
                print(log_message)
                raise  # Поднимаем исключение после логирования
            if filename:
                try:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                except Exception as e:
                    print(f"Error writing to log file: {e}")
            print(log_message)
            return result
        return wrapper

    return decorator


@log(filename="test_log.txt")
def my_function(x: int, y: int) -> int:
    return x + y
