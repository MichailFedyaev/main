import pytest

from src.processing import inform_state


@pytest.fixture()
def test_inform_state():
    return 'EXECUTED'


@pytest.fixture()
def test_inform_state1():
    return inform_state


@pytest.fixture()
def test_data():
    return "2018-07-11T02:26:18.671407"
