from src.decorators import log


def test_log_correct(capsys):
    # Проверка корректного выполнения функции
    @log(filename="test_log.txt")
    def my_function(x, y):
        return x + y

    my_function(1, 2)
    captured = capsys.readouterr()
    assert "my_function called with args: (1, 2), kwargs:{}. Result: 3\n" in captured.out


def test_log_different_types_str(capsys):
    # Проверка ошибки: missing 2 required positional arguments: 'x' and 'y'.
    @log(filename="test_log.txt")
    def my_function(x, y):
        return x + y

    try:
        my_function("a", "b")
    except TypeError as e:
        captured = capsys.readouterr()
        assert "my function error: " in captured.out


def test_log_lack_argument(capsys):
    # Проверка ошибки: missing 1 required positional argument: 'y'.
    @log(filename="test_log.txt")
    def my_function(x, y):
        return x + y

    try:
        my_function(1)
    except TypeError as e:
        captured = capsys.readouterr()
        expected_error_message = "my_function error: test_log_lack_argument.<locals>.my_function() missing 1 required positional argument: 'y'. Inputs:(1,), {}"
        assert expected_error_message in captured.out
        assert str(e) == "test_log_lack_argument.<locals>.my_function() missing 1 required positional argument: 'y'"


def test_log_different_types_argument(capsys):
    # Проверка ошибки: unsupported operand type(s) for +: 'int' and 'str'.
    @log(filename="test_log.txt")
    def my_function(x, y):
        return x + y

    try:
        my_function(1, "")
    except TypeError as e:
        captured = capsys.readouterr()
        expected_error_message = "my_function error: unsupported operand type(s) for +: 'int' and 'str'. Inputs:(1, ''), {}"
        assert expected_error_message in captured.out
        assert str(e) == "unsupported operand type(s) for +: 'int' and 'str'"


def test_log_different_types_no_argument(capsys):
    # Проверка ошибки: missing 2 required positional arguments: 'x' and 'y'.
    @log(filename="test_log.txt")
    def my_function(x, y):
        return x + y

    try:
        my_function()
    except TypeError as e:
        captured = capsys.readouterr()
        expected_error_message = "my_function error: test_log_different_types_no_argument.<locals>.my_function() missing 2 required positional arguments: 'x' and 'y'. Inputs:(), {}"
        assert expected_error_message in captured.out
        assert str(e) == "test_log_different_types_no_argument.<locals>.my_function() missing 2 required positional arguments: 'x' and 'y'"
