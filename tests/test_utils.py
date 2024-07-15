import pytest

from src.utils import get_transactions_dictionary, transaction_amount_in_rub


def test_get_transactions_dictionary(get_path):
    assert get_transactions_dictionary(get_path)[0] == {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  }


def test_get_transactions_dictionary1(get_wrong_path):
    assert get_transactions_dictionary(get_wrong_path) == []


def test_get_transactions_dictionary2(get_bad_file):
    assert get_transactions_dictionary(get_bad_file) == []


def test_transaction_amount_in_rub(transaction, rub_transaction_number):
    assert transaction_amount_in_rub(transaction, rub_transaction_number) == 860637.41

