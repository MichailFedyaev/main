from typing import Any

inform_state = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(inform_states: list[dict[str, Any]], states_id: str = "EXECUTED") -> list[dict[str, Any]]:
    """Функция фильтрации операций по ключу state"""
    list_stat = []
    for key in inform_states:
        if key.get("state") == states_id:
            list_stat.append(key)
    return list_stat


print(filter_by_state(inform_state))


def sort_by_date(inform_states: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Функция сортировки операций по дате"""
    sorted_inform_state = sorted(inform_states, key=lambda inform_states: inform_states["date"], reverse=reverse)
    return sorted_inform_state


print(sort_by_date(inform_state))
