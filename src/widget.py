from datetime import datetime
from typing import Any

from src.masks import mask_account, mask_card_number


def mask_account_card(card_or_account_inform: str) -> str:
    """ Функция, которая маскирует номер карту/счёт"""
    if card_or_account_inform is None:
        return ""
    try:
        # Получение типа и номера карты/счета
        card_or_account_type, card_or_account_num = card_or_account_inform.rsplit(" ", 1)
    except ValueError:
        return ""

    if card_or_account_type.lower() in ("счет", "счёт"):
        return f"{card_or_account_type} {mask_account(card_or_account_num)}"
    else:
        return f"{card_or_account_type} {mask_card_number(card_or_account_num)}"


def get_data(date_of_transaction: str) -> str:
    """Функция возвращает дату"""
    # Получение даты и времени
    date, _ = date_of_transaction.split("T")
    # Получение списка, элементами которого являются yy, mm, dd
    date_list = date.split("-")

    return f"{date_list[2]}.{date_list[1]}.{date_list[0]}"
