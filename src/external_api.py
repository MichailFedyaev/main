import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

api_key = os.getenv("API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции (amount) в рублях.

    :param transaction: Транзакция.
    :return: Сумма транзакции в рублях.
    """
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount
    else:
        url = f"https://api.apilayer.com/exchangerates_data/convert?from={currency}&to=RUB&amount={amount}"
        headers = {"apikey": api_key}

        response = requests.get(url, headers=headers)
        # Если запрос успешен, возвращается результат конвертации суммы
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "result" in data:
                return float(data["result"])

        raise ValueError(f"Failed to get the exchange rate for {currency} to RUB")
