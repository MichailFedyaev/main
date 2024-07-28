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
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        }
    ]


@pytest.fixture
def categories() -> list:
    return ["Перевод", "Вклад", "Организации"]


@pytest.fixture
def transaction2():
    return [
        {
            "operation_date": "27.09.2019 13:05:37",
            "payment_date": "29.09.2019",
            "card_number": "*7197",
            "status": "OK",
            "operation_sum": -144.45,
            "operation_cur": "RUB",
            "payment_sum": -144.45,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Супермаркеты",
            "MCC": 5499.0,
            "description": "Колхоз",
            "Bonus": 2,
            "Invest_bank": 0,
            "rounded_operation_sum": 144.45,
        },
        {
            "operation_date": "27.09.2019 04:17:51",
            "payment_date": "27.09.2019",
            "card_number": "*4556",
            "status": "OK",
            "operation_sum": 1000.0,
            "operation_cur": "RUB",
            "payment_sum": 1000.0,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Бонусы",
            "MCC": 0,
            "description": 'Пополнение. Тинькофф Банк. Бонус по акции "Приведи друга"',
            "Bonus": 0,
            "Invest_bank": 0,
            "rounded_operation_sum": 1000.0,
        },
        {
            "operation_date": "26.09.2019 18:12:45",
            "payment_date": "26.09.2019",
            "card_number": "*4556",
            "status": "OK",
            "operation_sum": 250.0,
            "operation_cur": "RUB",
            "payment_sum": 250.0,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Пополнения",
            "MCC": 0,
            "description": "Пополнение через Альфа-Банк",
            "Bonus": 0,
            "Invest_bank": 0,
            "rounded_operation_sum": 250.0,
        },
        {
            "operation_date": "26.09.2019 17:42:59",
            "payment_date": "28.09.2019",
            "card_number": "*7197",
            "status": "OK",
            "operation_sum": -177.1,
            "operation_cur": "RUB",
            "payment_sum": -177.1,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Супермаркеты",
            "MCC": 5411.0,
            "description": "SPAR",
            "Bonus": 3,
            "Invest_bank": 0,
            "rounded_operation_sum": 177.1,
        },
        {
            "operation_date": "26.09.2019 11:57:20",
            "payment_date": "27.09.2019",
            "card_number": "*7197",
            "status": "OK",
            "operation_sum": -357.22,
            "operation_cur": "RUB",
            "payment_sum": -357.22,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Отели",
            "MCC": 7011.0,
            "description": "Dongying Luxury Blue Hori",
            "Bonus": 7,
            "Invest_bank": 0,
            "rounded_operation_sum": 357.22,
        },
    ]