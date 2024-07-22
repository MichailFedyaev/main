from typing import List, Dict, Any
import json
from unittest.mock import mock_open, patch, Mock
from src.utils import get_transactions_dictionary, get_transactions_csv, get_transactions_excel
import pandas as pd


def test_get_transactions_dictionary_valid_file(transaction1: List[Dict[str, Any]]) -> None:
    # Преобразуем список транзакций в JSON-строку
    json_data = json.dumps(transaction1)

    # Используем mock_open для имитации открытия файла и чтения корректных данных
    mocked_open = mock_open(read_data=json_data)
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == transaction1
            mocked_open.assert_called_once_with("dummy_path.json")


@patch("src.utils.utils_logger")
def test_get_transactions_dictionary_logs_info(mock_logger: Mock, transaction1: List[Dict[str, Any]]) -> None:
    # Преобразуем список транзакций в JSON-строку
    json_data = json.dumps(transaction1)

    # Используем mock_open для имитации открытия файла и чтения корректных данных
    mocked_open = mock_open(read_data=json_data)
    with patch("builtins.open", mocked_open):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == transaction1
            mock_logger.info.assert_called_once_with("Successfully read file: dummy_path.json")


@patch("src.utils.utils_logger")
def test_get_transactions_dictionary_invalid_format_logs_warning(mock_logger: Mock) -> None:
    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data='{"invalid": "data"}')
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mock_logger.warning.assert_called_once_with("Invalid data format in file: dummy_path.json")


def test_get_transactions_dictionary_invalid_file() -> None:
    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data='{"invalid": "data"}')
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_empty_file() -> None:
    # Используем mock_open для имитации открытия пустого файла и чтения данных
    mocked_open = mock_open(read_data="")
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_nonexistent_file() -> None:
    # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала False
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        # Вызываем тестируемую функцию и проверяем результат
        result = get_transactions_dictionary("dummy_path.json")
        assert result == []
        mock_exists.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_json_decode_error() -> None:
    """Тестирует функцию get_transactions_dictionary с существующим JSON-файлом,
     содержащим некорректный формат JSON-данных."""
    # Используем mock_open для имитации открытия файла и чтения некорректного формата JSON-данных
    mocked_open = mock_open(read_data="invalid json")
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_json_io_error() -> None:
    # Используем контекстный менеджер path и аргумент side_effect для имитации открытия файла и генерации исключения
    with patch("builtins.open", side_effect=IOError):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mock_exists.assert_called_once_with("dummy_path.json")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_valid_file(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим CSV-файлом, содержащим корректные данные."""
    data = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])

    # Используем patch для имитации pandas.read_csv и os.path.exists
    with patch("pandas.read_csv", return_value=data) as mock_read_csv:
        with patch("os.path.exists", return_value=True):
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv")
            expected_result = data.to_dict(orient="records")
            assert result == expected_result
            mock_read_csv.assert_called_once_with("dummy_path.csv")
            mock_logger.info.assert_called_once_with("Successfully read CSV file: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_empty_file(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим пустым CSV-файлом."""
    # Используем patch для имитации pandas.read_csv и возвращения пустого DataFrame
    with patch("pandas.read_csv", return_value=pd.DataFrame()):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv")
            assert result == []
            mock_logger.warning.assert_called_once_with("File is empty or not a DataFrame: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_parse_error(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим CSV-файлом, содержащим некорректные данные."""
    csv_data = "id,amount\n1,100\n2,"

    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data=csv_data)
    with patch("builtins.open", mocked_open):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Используем контекстный менеджер и аргумент side_effect для имитации чтения и генерации исключения
            with patch("pandas.read_csv", side_effect=pd.errors.ParserError("Mock ParserError")):
                # Вызываем тестируемую функцию и проверяем результат
                result = get_transactions_csv("dummy_path.csv")
                assert result == []
                mock_logger.error.assert_called_once_with("ParserError: Failed to parse file: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_io_error(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим CSV-файлом и имитацией IOError."""
    # Используем контекстный менеджер pathc и аргумент side_effect для имитации открытия файла и генерации исключения
    with patch("builtins.open", side_effect=IOError("Mock IOError")):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv")
            assert result == []
            mock_logger.error.assert_called_once_with("Unexpected error: Mock IOError")


@patch("src.utils.utils_logger")
def test_get_transactions_excel_valid_file(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_excel с существующим Excel-файлом, содержащим корректные данные."""
    data = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])

    # Используем patch для имитации pandas.read_excel и os.path.exists
    with patch("pandas.read_excel", return_value=data) as mock_read_excel:
        with patch("os.path.exists", return_value=True):
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_excel("dummy_path.xlsx")
            expected_result = data.to_dict(orient="records")
            assert result == expected_result
            mock_read_excel.assert_called_once_with("dummy_path.xlsx")
            mock_logger.info.assert_called_once_with("Successfully read Excel file: dummy_path.xlsx")


@patch("src.utils.utils_logger")
def test_get_transactions_excel_empty_file(mock_logger: Mock) -> None:
    """Тестирует функцию get_transactions_excel с существующим пустым Excel-файлом."""
    empty_data = pd.DataFrame()

    # Используем patch для имитации pandas.read_excel и os.path.exists
    with patch("pandas.read_excel", return_value=empty_data) as mock_read_excel:
        with patch("os.path.exists", return_value=True):
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_excel("dummy_empty.xlsx")
            assert result == []
            mock_read_excel.assert_called_once_with("dummy_empty.xlsx")
            mock_logger.warning.assert_called_once_with("File is empty or not a DataFrame: dummy_empty.xlsx")


@patch("src.utils.utils_logger")
def test_get_transactions_excel_parse_error(mock_logger: Mock) -> None:
    """Тестирует функцию get_transactions_excel с существующим Excel-файлом, содержащим некорректные данные."""
    # Используем patch для имитации pandas.get_excel и генерации ValueError
    with patch("pandas.read_excel", side_effect=ValueError("Mock ValueError")):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_excel("dummy_path.xlsx")
            assert result == []
            mock_logger.error.assert_called_once_with("ValueError: Failed to parse file: dummy_path.xlsx")


@patch("src.utils.utils_logger")
def test_get_transactions_excel_io_error(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_excel с существующим Excel-файлом и имитацией IOError."""
    # Используем контекстный менеджер pathc и аргумент side_effect для имитации чтения файла и генерации исключения
    with patch("pandas.read_excel", side_effect=IOError("Mock IOError")):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_excel("dummy_path.xlsx")
            assert result == []
            mock_logger.error.assert_called_once_with("Unexpected error: Mock IOError")
