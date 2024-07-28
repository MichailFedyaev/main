import datetime
import json
from typing import Any

from src.logger_setup import setup_logger

services_logger = setup_logger(__name__)


def investment_bank(month: str, transactions: list | Any, limit: int) -> str:
    """Рассчитывает сумму на счету инвесткопилки по заданному порогу округления"""
    services_logger.info("Start")
    period = datetime.datetime.strptime(month, "%Y-%m")
    services_logger.info("Creating a list of filtered transactions")
    transactions_list = []
    investment_bank_sum = 0
    services_logger.info("Filtering transactions by date and adding their amount to the list of filtered transactions")
    for transaction in transactions:
        transaction_date = transaction["operation_date"]
        payment_date = datetime.datetime.strptime(transaction_date, "%d.%m.%Y %H:%M:%S")
        if payment_date.month == period.month and transaction["payment_sum"] < 0:
            transactions_list.append(transaction["payment_sum"])
    services_logger.info("Calculation of the remaining amount for the investment bank")
    for transact in transactions_list:
        sum = abs(transact)
        diff = (sum // limit + 1) * limit - sum
        investment_bank_sum += diff
    services_logger.info("Creating a json file with the amount for the investment bank")
    result_list = []
    result_dict = {}
    result_dict["investment_bank"] = round(investment_bank_sum, 2)
    result_list.append(result_dict)
    result_list_jsons = json.dumps(result_list)
    services_logger.info("Stop")
    return result_list_jsons


# transactions = get_xlsx_data_dict("../data/operations.xlsx")
# result = investment_bank("2021-12", transactions, 50)
# print(result)
