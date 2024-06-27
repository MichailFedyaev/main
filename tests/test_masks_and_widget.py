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
