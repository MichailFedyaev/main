import json
from typing import Any

from src.logger_setup import setup_logger
from src.utils import (fetch_and_show_currency_rates, get_greeting, get_xlsx_data_dict, show_cards,
                       show_top_5_transactions)

views_logger = setup_logger(__name__)


def main_page(date: str) -> Any:
    """Записывает информацию для Главной страницы в файл json"""
    views_logger.info("Start")
    views_logger.info("Converting an Excel file to a dictionary list")
    transactions = get_xlsx_data_dict("../data/operations.xlsx")
    views_logger.info("Receiving a greeting")
    greeting = get_greeting(date)
    views_logger.info("Getting information about the card")
    cards = show_cards(date, transactions)
    views_logger.info("Getting the best deals")
    top_transcations = show_top_5_transactions(date, transactions)
    views_logger.info("Getting currency exchange rates")
    currency_rates = fetch_and_show_currency_rates()
    views_logger.info("Creating a dictionary of dictionaries")
    main_dict: dict = {}
    main_dict["greeting"] = greeting
    main_dict["cards"] = cards
    main_dict["top_transcations"] = top_transcations
    main_dict["currency_rates"] = currency_rates
    views_logger.info("Writing information to a json file")
    main_dict_jsons = json.dumps(main_dict, ensure_ascii=False)
    views_logger.info("Stop")
    return main_dict_jsons
