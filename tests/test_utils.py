from typing import List, Dict, Any
import json
from unittest.mock import mock_open, patch
from src.utils import get_transactions_dictionary


def test_get_transactions_dictionary_valid_file(transactions: List[Dict[str, Any]]) -> None:
    """Тестирует функцию get_transactions_dictionary с существующим JSON-файлом, содержащим корректные данные."""
    # Преобразуем список транзакций в JSON-строку
    json_data = json.dumps(transactions)

    # Используем mock_open для имитации открытия файла и чтения корректных данных
    mocked_open = mock_open(read_data=json_data)
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == transactions
            mocked_open.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_invalid_file() -> None:
    """Тестирует функцию get_transactions_dictionary с существующим JSON-файлом, содержащим некорректные данные."""
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
            mocked_open.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_nonexistent_file() -> None:
    """Тестирует функцию get_transactions_dictionary с несуществующим JSON-файлом."""
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
    """Тестирует функцию read_transactions_json с существующим JSON-файлом при возникновении ошибки IOError."""
    # Используем контекстный менеджер path и аргумент side_effect для имитации открытия файла и генерации исключения
    with patch("builtins.open", side_effect=IOError):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mock_exists.assert_called_once_with("dummy_path.json")
