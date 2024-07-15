import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")


def convert_to_rub(amount: float, currency: str) -> Any:
    """Функция принимает значение в долларах или евро, обращается к API и возвращает конвертацию в рубли"""
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_result = response.json()
        rub_amount = json_result["result"]
        return rub_amount
    else:
        raise Exception(f"Failed to convert currency: {response.status_code}")


# Пример использования функций
#if __name__ == "__main__":
   # try:
       # amount_in_rub = convert_to_rub(20, 'USD')
       # print(amount_in_rub)
   #except Exception as e:
        #print(e)