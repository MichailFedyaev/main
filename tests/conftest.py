import pytest

from src.processing import inform_state

from src.generators import transactions

from src.utils import get_transactions_dictionary


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


@pytest.fixture()
def get_path():
    return "D:/PycharmProject/main/data/operations.json"


@pytest.fixture()
def get_wrong_path():
    return "Nothing"


@pytest.fixture()
def get_bad_file():
    return '../data/wrong_operations.json'


@pytest.fixture()
def transaction():
    return get_transactions_dictionary("D:/PycharmProject/main/data/operations.json")


@pytest.fixture()
def rub_transaction_number():
    return 939719570
