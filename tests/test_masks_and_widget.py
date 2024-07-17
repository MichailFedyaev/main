from unittest.mock import Mock, patch

import pytest

from src.masks import mask_account, mask_card_number

from src.widget import mask_account_card, get_data


@pytest.mark.parametrize('string, expected_result', [
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счет 12345678901234567890", "Счет **7890"),
])
def test_mask_account_card(string, expected_result):
    assert mask_account_card(string) == expected_result


def test_get_data(test_data):
    assert get_data(test_data) == "11.07.2018"


@pytest.mark.parametrize('string, expected_result', [
    ("12345678901234567340", "**7340"),
    ("12345678901234567890", "**7890"),
])
def test_mask_account(string, expected_result):
    assert mask_account(string) == expected_result


@pytest.mark.parametrize('string, expected_result', [
    ("7158300734726758", "7158 30** **** 6758"),
    ("7158300734726759", "7158 30** **** 6759"),
])
def test_mask_card_number(string, expected_result):
    assert mask_card_number(string) == expected_result


@patch("src.masks.masks_logger")
def test_get_mask_card_number_logs_info(mock_logger: Mock, card_number: str) -> None:
    """Тестирует, что функция mask_card_number логирует корректное сообщение."""
    assert mask_card_number("7000792289606361") == card_number
    mock_logger.info.assert_called_once_with(f"Masked card number: {card_number}")


@patch("src.masks.masks_logger")
def test_get_mask_account_logs_info(mock_logger: Mock) -> None:
    """Тестирует, что функция mask_account логирует корректное сообщение."""
    assert mask_account("73654108430135874305") == "**4305"
    mock_logger.info.assert_called_once_with("Masked account number: **4305")
