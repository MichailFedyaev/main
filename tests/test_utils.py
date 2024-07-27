from typing import List, Dict, Any
import json
from unittest import mock
from unittest.mock import mock_open, patch, Mock
from src.utils import get_transactions_dictionary, get_transactions_csv, get_transactions_excel
import pandas as pd
import os
import openpyxl


def test_get_transactions_dictionary_valid_file(transaction1: List[Dict[str, Any]]) -> None:
    """ Тестирует функцию get_transactions_json с существующим JSON-файлом, содержащим корректные данные."""
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
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


@patch("src.utils.utils_logger")
def test_get_transactions_dictionary_logs_info(mock_logger: Mock, transaction1: List[Dict[str, Any]]) -> None:
    """ Тестирует, что функция read_transactions_json логирует корректное сообщение при успешном чтении файла."""
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
    """ Тестирует функцию get_transactions_json с существующим JSON-файлом, содержащим некорректные данные."""
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
    """Тестирует, что функция get_transactions_json логирует сообщение предупреждение
     при некорректном формате данных."""
    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data='{"invalid": "data"}')
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


def test_get_transactions_dictionary_empty_file() -> None:
    """ Тестирует функцию read_transactions_json с существующим пустым JSON-файлом."""
    # Используем mock_open для имитации открытия пустого файла и чтения данных
    mocked_open = mock_open(read_data="")
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


def test_get_transactions_dictionary_nonexistent_file() -> None:
    """Тестирует функцию read_transactions_json с несуществующим JSON-файлом."""
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
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


def test_get_transactions_dictionary_json_io_error() -> None:
    """ Тестирует функцию read_transactions_json с существующим JSON-файлом, содержащим
     некорректный формат JSON-данных."""
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
            mock_read_csv.assert_called_once_with("dummy_path.csv", delimiter=';')
            mock_logger.info.assert_called_once_with("Successfully read CSV file: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_empty_file(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим пустым CSV-файлом."""
    # Используем patch для имитации pandas.read_csv и возвращения пустого DataFrame
    with patch("pandas.read_csv", return_value=pd.DataFrame()):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv",)
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
                result = get_transactions_csv("dummy_path.csv",)
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


# Тест на отсутствие файла
def test_get_transactions_excel_file_not_found():
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = False
        result = get_transactions_excel("nonexistent_file.xlsx")
        assert result == []


# Тест на неверный формат файла
def test_get_transactions_excel_invalid_file_format():
    with patch("openpyxl.load_workbook") as mock_load_workbook:
        mock_load_workbook.side_effect = openpyxl.utils.exceptions.InvalidFileException
        result = get_transactions_excel("invalid_format.xlsx")
        assert result == []


# Тест на пустой файл
def test_get_transactions_excel_empty_file():
    with patch("openpyxl.load_workbook") as mock_load_workbook:
        mock_sheet = mock_load_workbook().active
        mock_sheet.iter_rows.return_value = []
        result = get_transactions_excel("empty_file.xlsx")
        assert result == []
