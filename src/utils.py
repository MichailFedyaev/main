import json
import os
from typing import Any, List, Dict
from src.logger_setup import setup_logger

# Создание и получение именованного логгера
utils_logger = setup_logger(__name__)


def get_transactions_dictionary(file_path: str) -> List[Dict[str, Any]]:
    """Функция принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    if not os.path.exists(file_path):
        utils_logger.warning(f"File {file_path} does not exist.")
        return []

    try:
        with open(file_path) as operations:
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


#if __name__ == "__main__":
    #В лог записывается что такого файла не существует)
    #transact = get_transactions_dictionary("D:/PycharmProject/non-existent/data/operations.json")
    #print(transact)