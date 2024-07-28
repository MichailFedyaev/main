import datetime
import json
import os
from typing import Any, Dict, Hashable, List

import openpyxl
import pandas as pd
import requests
from dotenv import load_dotenv
from requests import RequestException

from src.logger_setup import setup_logger

# Создание и получение именованного логгера
utils_logger = setup_logger(__name__)

load_dotenv()

api_key = os.getenv("API_KEY")


def get_xlsx_data_dict(file_name: str) -> list[dict] | str:
    """Считывает данные о финансовых операциях из excel файла и преобразует их в список словарей"""
    try:
        xlsx_data = pd.read_excel(file_name)
        data_list = xlsx_data.apply(
            lambda row: {
                "operation_date": row["Дата операции"],
                "payment_date": row["Дата платежа"],
                "card_number": row["Номер карты"],
                "status": row["Статус"],
                "operation_sum": row["Сумма операции"],
                "operation_cur": row["Валюта операции"],
                "payment_sum": row["Сумма платежа"],
                "payment_cur": row["Валюта платежа"],
                "cashback": row["Кэшбэк"],
                "category": row["Категория"],
                "MCC": row["MCC"],
                "description": row["Описание"],
                "Bonus": row["Бонусы (включая кэшбэк)"],
                "Invest_bank": row["Округление на инвесткопилку"],
                "rounded_operation_sum": row["Сумма операции с округлением"],
            },
            axis=1,
        )
        new_dict_list = []
        row_index = 0
        for row in data_list:
            new_dict_list.append(data_list[row_index])
            row_index += 1
        return new_dict_list

    except Exception:
        return "File can't be read"


def get_greeting(time_data: str) -> str:
    """Принимает текущее время и возвращает приветствие в зависимости от времени суток"""
    if 0 <= int(time_data[11:13]) <= 5:
        return "Доброй ночи"
    elif 6 <= int(time_data[11:13]) <= 11:
        return "Доброе утро"
    elif 12 <= int(time_data[11:13]) <= 17:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_time_data() -> str:
    """Возвращает текущее время"""
    time_data = datetime.datetime.now()
    return str(time_data)


def get_card_number_list(transactions: list[dict[Any, Any]]) -> list:
    """Выводит список уникальных номеров карт из списка транзакций"""
    card_list_full = []
    for transaction in transactions:
        if transaction["card_number"]:
            card_list_full.append(transaction["card_number"])
    card_list_short = []
    for card in card_list_full:
        if card not in card_list_short and type(card) is str:
            card_list_short.append(card)
    return card_list_short


def get_operations_sum(time_data: str, transactions: list[dict[str, Any]], card_number: str) -> Any:
    """Выводит общую сумму расходов по номеру карты в формате *1234"""
    month = time_data[5:7] + "." + time_data[:4]
    transactions_sum_list = []
    for transaction in transactions:
        date = str(transaction["payment_date"])
        if transaction["card_number"] == card_number and date[3:] == month and transaction["payment_sum"] < 0:
            transactions_sum_list.append(transaction["payment_sum"])
    total_operations_sum = abs(sum(transactions_sum_list))
    return total_operations_sum


def get_cashback_sum(operations_sum: float) -> float:
    """Высчитывает процент кэшбэка от общей суммы(1%)"""
    cash_back_sum = round(operations_sum / 100, 2)
    return cash_back_sum


def show_cards(time_data: str, transactions: list | Any) -> list[dict]:
    """Выводит информацию по каждой карте (последние 4 цифры карты, общая сумма расходов, кэшбэк)"""
    show_cards_list = []
    cards_list = get_card_number_list(transactions)
    for card in cards_list:
        total_spent = get_operations_sum(time_data, transactions, card)
        card_dict = {}
        card_dict["last_digits"] = card[1:]
        card_dict["total_spent"] = get_operations_sum(time_data, transactions, card)
        card_dict["cashback"] = get_cashback_sum(total_spent)
        show_cards_list.append(card_dict)
    return show_cards_list


def show_top_5_transactions(time_data: str, transactions: list | Any) -> list[dict[str, Any]]:
    """Выводит информацию о 5 топ транзакциях по сумме платежа"""
    for transaction in transactions:
        neg_sum = transaction["payment_sum"]
        transaction["payment_sum"] = abs(neg_sum)
    month = time_data[5:7] + "." + time_data[:4]
    month_transactions = []
    for transaction in transactions:
        date = str(transaction["payment_date"])
        if date[3:] == month:
            month_transactions.append(transaction)
    sorted_transactions = sorted(
        month_transactions,
        key=lambda transaction: transaction["payment_sum"],
        reverse=True,
    )
    list_index = 1
    top_5_transactions = []
    for transaction in sorted_transactions:
        if list_index < 6:
            top_transaction_dict = {}
            top_transaction_dict["date"] = transaction["payment_date"]
            top_transaction_dict["amount"] = transaction["payment_sum"]
            top_transaction_dict["category"] = transaction["category"]
            top_transaction_dict["description"] = transaction["description"]
            top_5_transactions.append(top_transaction_dict)
            list_index += 1
    return top_5_transactions


def fetch_and_show_currency_rates() -> list[dict[str, Any]]:
    """Выводит курс валют и записывает из в файл .json"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        #        payload = {}
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        print(response)
        result = response.json()
        print(result)
        exchange_rates_list = []
        usd_rate = {"currency": "USD", "rate": round(result["Valute"]["USD"]["Value"], 2)}
        eur_rate = {"currency": "EUR", "rate": round(result["Valute"]["EUR"]["Value"], 2)}
        exchange_rates_list.append(usd_rate)
        exchange_rates_list.append(eur_rate)
        with open("user_settings.json", "w") as f:
            json.dump(exchange_rates_list, f)
        return exchange_rates_list
    except RequestException:
        return [{}]


def get_transactions_dictionary(file_path: str) -> List[Dict[Hashable, Any]]:
    """Функция принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    if not os.path.exists(file_path):
        utils_logger.warning(f"File {file_path} does not exist.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as operations:
            transaction_data = json.load(operations)
            if isinstance(transaction_data, list):
                utils_logger.info(f"Successfully read file: {file_path}")
                return transaction_data
            else:
                utils_logger.warning(f"Invalid data format in file: {file_path}")
                return []

    except (json.JSONDecodeError, IOError) as e:
        utils_logger.error(f"Error reading file {file_path}: {e}")
        return []


def get_transactions_csv(
    file_path: str,
) -> List[Dict[Hashable, Any]]:
    """Функция принимает путь до CSV-файла и возвращает список словарей с данными о финансовых транзакциях."""
    if not os.path.exists(file_path):
        utils_logger.warning(f"File does not exist: {file_path}")
        return []

    try:
        df = pd.read_csv(
            file_path,
            delimiter=";",
        )
        if df.empty or not isinstance(df, pd.DataFrame):
            utils_logger.warning(f"File is empty or not a DataFrame: {file_path}")
            return []
        # Заполняем NaN пустыми строками
        df = df.fillna("")
        utils_logger.info(f"Successfully read CSV file: {file_path}")
        return df.to_dict(orient="records")

    except pd.errors.EmptyDataError:
        utils_logger.error(f"EmptyDataError: File is empty: {file_path}")
        return []

    except pd.errors.ParserError:
        utils_logger.error(f"ParserError: Failed to parse file: {file_path}")
        return []

    except Exception as e:
        utils_logger.error(f"Unexpected error: {e}")
        return []


def get_transactions_excel(file_path):
    """Функция принимает путь до EXEL-файла и возвращает список словарей с данными о финансовых транзакциях."""
    if not os.path.isfile(file_path):
        print(f"Ошибка: {file_path} не является файлом.")
        return []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        transactions = []
        headers = [cell.value for cell in sheet[1]]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            transaction = {headers[i]: row[i] for i in range(len(headers))}
            transactions.append(transaction)
        return transactions
    except (FileNotFoundError, openpyxl.utils.exceptions.InvalidFileException, PermissionError) as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []
