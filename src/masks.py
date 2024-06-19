from typing import Any


def mask_card_number(card_number: str) -> Any:
    """Функция, маскировки номера карты"""
    masked_number = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
    return masked_number


def mask_account(account_number: str) -> Any:
    """Функция, маскировки номера счета"""
    account_number = account_number.replace(" ", "")
    if not account_number.isdigit() or len(account_number) < 4:
        return "Invalid account number"
    masked_number = "**" + account_number[-4:]
    return masked_number
