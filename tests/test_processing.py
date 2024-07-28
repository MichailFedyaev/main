import pytest

from src.processing import (filter_by_state, sort_by_date, inform_state, search_transactions,
                            count_transactions_by_category)
from collections import Counter
from typing import List, Dict, Any


@pytest.mark.parametrize("records, state, expected", [
    (
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
        'EXECUTED',
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    ),
    (
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
        'CANCELED',
        [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    )
])
def test_filter_by_state(records, state, expected):
    assert filter_by_state(records, state) == expected


test_processing = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]


def test_filter_by_state1(test_inform_state1):
    assert filter_by_state(inform_state) == test_processing


def test_sort_by_date(test_inform_state1):
    assert sort_by_date(inform_state) == [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                                          {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                                          {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                                          {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]


def test_search_transactions(transaction1: List[Dict[str, Any]]) -> None:
    """Тестирует поиск по описанию."""
    result = search_transactions(transaction1, "Перевод организации")
    assert len(result) == 2
    assert result[0]["id"] == 441945886
    assert result[1]["id"] == 41428829


def test_search_transactions_by_piece(transaction1: List[Dict[str, Any]]) -> None:
    """Тестирует поиск по части слова."""
    result = search_transactions(transaction1, "вкл")
    assert len(result) == 1
    assert result[0]["id"] == 587085106


def test_search_transactions_no_result(transaction1: List[Dict[str, Any]]) -> None:
    """Тестирует поиск без нахождения транзакций."""
    result = search_transactions(transaction1, "покупка")
    assert len(result) == 0


def test_search_transactions_ignorecase(transaction1: List[Dict[str, Any]]) -> None:
    """Тестирует поиск без учета регистра."""
    result = search_transactions(transaction1, "СчЕт")
    assert len(result) == 1
    assert result[0]["id"] == 142264268


def test_count_transactions_by_category(transaction1: List[Dict[str, Any]], categories: list) -> None:
    """Тестирует подсчет транзакций по категориям."""
    result = count_transactions_by_category(transaction1, categories)
    expected = Counter({'Перевод': 3, 'Организации': 2, 'Вклад': 1})
    assert result == expected


def test_count_transactions_by_category_non_existent(transaction1: List[Dict[str, Any]]) -> None:
    """Тестирует подсчет транзакций по категориям, не содержащимся в описании транзакций."""
    result = count_transactions_by_category(transaction1, ["Недвижимость", "Инвестиции"])
    assert result == Counter()


def test_count_transactions_by_category_without_transactions(categories: list) -> None:
    """Тестируем случай, когда нет транзакций."""
    result = count_transactions_by_category([], categories)
    assert result == Counter()


def test_count_transactions_by_category_without_categories(transaction1: List[Dict[str, Any]]) -> None:
    """Тестируем случай, когда нет категорий."""
    result = count_transactions_by_category(transaction1, [])
    assert result == Counter()