import pytest

from src.processing import inform_state

from src.generators import transactions

from typing import Any, Dict, List


@pytest.fixture
def card_number() -> str:
    return "7000 79** **** 6361"


@pytest.fixture()
def test_inform_state():
    return 'EXECUTED'


@pytest.fixture()
def test_inform_state1():
    return inform_state


@pytest.fixture()
def test_data():
    return "2018-07-11T02:26:18.671407"


@pytest.fixture()
def test_transactions():
    return transactions


@pytest.fixture
def transaction1() -> List[Dict[str, Any]]:
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "100000", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]
