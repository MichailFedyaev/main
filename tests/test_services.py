import pytest
import json

from src.services import investment_bank


def test_investment_bank(transaction2):
    assert investment_bank("2021-12", transaction2, 50) == '[{"investment_bank": 0}]'


test_transactions = [
    {
        "operation_date": "15.01.2023 12:30:00",
        "payment_sum": -123.45
    },
    {
        "operation_date": "16.01.2023 14:45:00",
        "payment_sum": -67.89
    },
    {
        "operation_date": "17.02.2023 10:15:00",
        "payment_sum": -50.00
    }
]


def test_investment_bank_basic():
    month = "2023-01"
    limit = 10
    result = investment_bank(month, test_transactions, limit)
    result_dict = json.loads(result)[0]
    assert result_dict["investment_bank"] == 8.66  # Исправленное значение


def test_investment_bank_no_transactions():
    month = "2023-02"
    limit = 10
    result = investment_bank(month, [], limit)
    result_dict = json.loads(result)[0]
    assert result_dict["investment_bank"] == 0


def test_investment_bank_different_limit():
    month = "2023-01"
    limit = 5
    result = investment_bank(month, test_transactions, limit)
    result_dict = json.loads(result)[0]
    assert result_dict["investment_bank"] == 3.66


def test_investment_bank_zero_limit():
    month = "2023-01"
    limit = 0
    with pytest.raises(ZeroDivisionError):
        investment_bank(month, test_transactions, limit)


def test_investment_bank_invalid_date_format():
    month = "2023-01"
    limit = 10
    invalid_transactions = [
        {
            "operation_date": "15/01/2023 12:30:00",  # Неверный формат даты
            "payment_sum": -123.45
        }
    ]
    with pytest.raises(ValueError):
        investment_bank(month, invalid_transactions, limit)