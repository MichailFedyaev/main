import pytest
from src.external_api import convert_to_rub, api_key

from typing import Any, Dict, List, Union

from unittest.mock import patch, Mock


def test_convert_to_rub_success(transactions: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция convert_to_rub возвращает правильную сумму транзакции в рублях,
    если запрос к API прошел успешно и был получен корректный ответ."""
    transaction = transactions[1]  # USD

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": "8740.0"}
        mock_get.return_value = mock_response

        result = convert_to_rub(transaction)

        assert result == 8740.0
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?from=USD&to=RUB&amount=100.0",
            headers={"apikey": api_key},
        )


def test_convert_to_rub_failure(transactions: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция convert_to_rub выбрасывает исключение ValueError,
    если запрос к API завершился с ошибкой."""
    transaction = transactions[1]  # USD

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            convert_to_rub(transaction)

        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?from=USD&to=RUB&amount=100.0",
            headers={"apikey": api_key},
        )


def test_convert_to_rub_invalid_response(transactions: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция convert_to_rub выбрасывает исключение ValueError,
    если ответ от API содержит ошибку."""
    transaction = transactions[1]  # USD

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "error": {"code": 123, "message": "Invalid request"}}
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            convert_to_rub(transaction)

        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?from=USD&to=RUB&amount=100.0",
            headers={"apikey": api_key},
        )


def test_convert_to_rub_in_rub(transactions: List[Dict[str, Any]]) -> None:
    """ Проверяет, что функция convert_to_rub корректно обрабатывает транзакции в рублях."""
    transaction = transactions[0]  # RUB
    result = convert_to_rub(transaction)
    assert result == 100000.0
