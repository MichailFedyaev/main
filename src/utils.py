import json
from typing import Any
from src.external_api import convert_to_rub


def get_transactions_dictionary(path: str) -> Any:
    """Функция принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(path, "r", encoding="utf-8") as operations:
            try:
                transaction_data = json.load(operations)
                return transaction_data
            except json.JSONDecodeError:
                transaction_data = []
                return transaction_data
    except FileNotFoundError:
        transaction_data = []
        return transaction_data


def transaction_amount_in_rub(transactions: list, transaction_id: int) -> Any:
    """Функция принимает транзакцию и возвращает сумму транзакции в рублях, если не в рублях, конвертирует в рубли"""
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            amount = float(transaction["operationAmount"]["amount"])
            currency_code = transaction["operationAmount"]["currency"]["code"]

            if currency_code == "RUB":
                return amount
            elif currency_code == "USD":
                rub_amount = round(convert_to_rub(amount, currency_code), 2)
                return rub_amount
            elif currency_code == "EUR":
                rub_amount = round(convert_to_rub(amount, currency_code), 2)
                return rub_amount

#if __name__ == "__main__":
    #try:
       #transact = get_transactions_dictionary("../data/operations.json")
       #print(transaction_amount_in_rub(transact, 939719570))
   # except Exception as e:
        #print(e)
