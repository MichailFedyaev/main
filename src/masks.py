from typing import Any
from src.logger_setup import setup_logger

# Создание и получение именованного логгера
masks_logger = setup_logger(__name__)


def mask_card_number(card_number: str) -> Any:
    """Функция, маскировки номера карты"""
    masked_number = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
    masks_logger.info(f"Masked card number: {masked_number}")
    return masked_number


def mask_account(account_number: str) -> Any:
    """Функция, маскировки номера счета"""
    account_number = account_number.replace(" ", "")
    if not account_number.isdigit() or len(account_number) < 4:
        return "Invalid account number"
    masked_number = "**" + account_number[-4:]
    masks_logger.info(f"Masked account number: {masked_number}")
    return masked_number
