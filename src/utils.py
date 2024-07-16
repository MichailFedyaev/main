import json
import os
from typing import Any, List, Dict


def get_transactions_dictionary(file_path: str) -> List[Dict[str, Any]]:
    """Функция принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path) as operations:
            transaction_data = json.load(operations)
            if isinstance(transaction_data, list):
                return transaction_data
            else:
                return []

    except (json.JSONDecodeError, IOError):
        return []
