import json
import os
from typing import Any, List, Dict, Hashable
from src.logger_setup import setup_logger
import pandas as pd

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


def get_transactions_csv(file_path: str) -> List[Dict[Hashable, Any]]:
    """ Функция принимает путь до CSV-файла и возвращает список словарей с данными о финансовых транзакциях."""
    if not os.path.exists(file_path):
        utils_logger.warning(f"File does not exist: {file_path}")
        return []

    try:
        df = pd.read_csv(file_path)
        if df.empty or not isinstance(df, pd.DataFrame):
            utils_logger.warning(f"File is empty or not a DataFrame: {file_path}")
            return []
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


def get_transactions_excel(file_path: str) -> List[Dict[Hashable, Any]]:
    """ Функция принимает путь до EXEL-файла и возвращает список словарей с данными о финансовых транзакциях."""
    if not os.path.exists(file_path):
        utils_logger.warning(f"File does not exist: {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        if df.empty or not isinstance(df, pd.DataFrame):
            utils_logger.warning(f"File is empty or not a DataFrame: {file_path}")
            return []
        utils_logger.info(f"Successfully read Excel file: {file_path}")
        return df.to_dict(orient="records")

    except pd.errors.EmptyDataError:
        utils_logger.error(f"EmptyDataError: File is empty: {file_path}")
        return []

    except ValueError:
        utils_logger.error(f"ValueError: Failed to parse file: {file_path}")
        return []

    except Exception as e:
        utils_logger.error(f"Unexpected error: {e}")
        return []
