import re
from collections import Counter
from typing import Any, Dict, List

inform_state = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(records: list, state: str = "EXECUTED") -> list:
    """Фильтрует операции по заданному состоянию."""
    return [record for record in records if state == record.get("state")]


def sort_by_date(inform_states: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Функция сортировки операций по дате"""
    sorted_inform_state = sorted(inform_states, key=lambda inform_states: inform_states["date"], reverse=reverse)
    return sorted_inform_state


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Ищет транзакции, в описании которых содержится заданная строка поиска."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество транзакций для каждой категории на основе описаний транзакций."""
    categories_lower = [category.lower() for category in categories]
    categories_used = []
    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for category in categories_lower:
            if category in description:
                categories_used.append(category)
    # Преобразование категорий обратно в исходный регистр и возвращение результата
    return Counter([categories[categories_lower.index(category)] for category in categories_used])
