from typing import List, Dict, Any
import json
from unittest import mock
from unittest.mock import mock_open, patch, Mock

import pytest

from src.utils import (get_transactions_dictionary, get_transactions_csv, fetch_and_show_currency_rates,
                       get_card_number_list, get_transactions_excel, get_cashback_sum, get_greeting,
                       get_operations_sum, get_xlsx_data_dict, show_cards, show_top_5_transactions)

import pandas as pd
import os
import openpyxl
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_KEY")


def test_get_transactions_dictionary_valid_file(transaction1: List[Dict[str, Any]]) -> None:
    """ Тестирует функцию get_transactions_json с существующим JSON-файлом, содержащим корректные данные."""
    # Преобразуем список транзакций в JSON-строку
    json_data = json.dumps(transaction1)

    # Используем mock_open для имитации открытия файла и чтения корректных данных
    mocked_open = mock_open(read_data=json_data)
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == transaction1
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


@patch("src.utils.utils_logger")
def test_get_transactions_dictionary_logs_info(mock_logger: Mock, transaction1: List[Dict[str, Any]]) -> None:
    """ Тестирует, что функция read_transactions_json логирует корректное сообщение при успешном чтении файла."""
    # Преобразуем список транзакций в JSON-строку
    json_data = json.dumps(transaction1)

    # Используем mock_open для имитации открытия файла и чтения корректных данных
    mocked_open = mock_open(read_data=json_data)
    with patch("builtins.open", mocked_open):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == transaction1
            mock_logger.info.assert_called_once_with("Successfully read file: dummy_path.json")


@patch("src.utils.utils_logger")
def test_get_transactions_dictionary_invalid_format_logs_warning(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_json с существующим JSON-файлом, содержащим некорректные данные."""
    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data='{"invalid": "data"}')
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mock_logger.warning.assert_called_once_with("Invalid data format in file: dummy_path.json")


def test_get_transactions_dictionary_invalid_file() -> None:
    """Тестирует, что функция get_transactions_json логирует сообщение предупреждение
     при некорректном формате данных."""
    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data='{"invalid": "data"}')
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


def test_get_transactions_dictionary_empty_file() -> None:
    """ Тестирует функцию read_transactions_json с существующим пустым JSON-файлом."""
    # Используем mock_open для имитации открытия пустого файла и чтения данных
    mocked_open = mock_open(read_data="")
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


def test_get_transactions_dictionary_nonexistent_file() -> None:
    """Тестирует функцию read_transactions_json с несуществующим JSON-файлом."""
    # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала False
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        # Вызываем тестируемую функцию и проверяем результат
        result = get_transactions_dictionary("dummy_path.json")
        assert result == []
        mock_exists.assert_called_once_with("dummy_path.json")


def test_get_transactions_dictionary_json_decode_error() -> None:
    """Тестирует функцию get_transactions_dictionary с существующим JSON-файлом,
     содержащим некорректный формат JSON-данных."""
    # Используем mock_open для имитации открытия файла и чтения некорректного формата JSON-данных
    mocked_open = mock_open(read_data="invalid json")
    with patch("builtins.open", mocked_open):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mocked_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')


def test_get_transactions_dictionary_json_io_error() -> None:
    """ Тестирует функцию read_transactions_json с существующим JSON-файлом, содержащим
     некорректный формат JSON-данных."""
    # Используем контекстный менеджер path и аргумент side_effect для имитации открытия файла и генерации исключения
    with patch("builtins.open", side_effect=IOError):
        # Используем patch для имитации os.path.exists и задаем, чтобы она возвращала True
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_dictionary("dummy_path.json")
            assert result == []
            mock_exists.assert_called_once_with("dummy_path.json")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_valid_file(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим CSV-файлом, содержащим корректные данные."""
    data = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])

    # Используем patch для имитации pandas.read_csv и os.path.exists
    with patch("pandas.read_csv", return_value=data) as mock_read_csv:
        with patch("os.path.exists", return_value=True):
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv")
            expected_result = data.to_dict(orient="records")
            assert result == expected_result
            mock_read_csv.assert_called_once_with("dummy_path.csv", delimiter=';')
            mock_logger.info.assert_called_once_with("Successfully read CSV file: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_empty_file(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим пустым CSV-файлом."""
    # Используем patch для имитации pandas.read_csv и возвращения пустого DataFrame
    with patch("pandas.read_csv", return_value=pd.DataFrame()):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv",)
            assert result == []
            mock_logger.warning.assert_called_once_with("File is empty or not a DataFrame: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_parse_error(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим CSV-файлом, содержащим некорректные данные."""
    csv_data = "id,amount\n1,100\n2,"

    # Используем mock_open для имитации открытия файла и чтения некорректных данных
    mocked_open = mock_open(read_data=csv_data)
    with patch("builtins.open", mocked_open):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Используем контекстный менеджер и аргумент side_effect для имитации чтения и генерации исключения
            with patch("pandas.read_csv", side_effect=pd.errors.ParserError("Mock ParserError")):
                # Вызываем тестируемую функцию и проверяем результат
                result = get_transactions_csv("dummy_path.csv",)
                assert result == []
                mock_logger.error.assert_called_once_with("ParserError: Failed to parse file: dummy_path.csv")


@patch("src.utils.utils_logger")
def test_get_transactions_csv_io_error(mock_logger: Mock) -> None:
    """ Тестирует функцию get_transactions_csv с существующим CSV-файлом и имитацией IOError."""
    # Используем контекстный менеджер pathc и аргумент side_effect для имитации открытия файла и генерации исключения
    with patch("builtins.open", side_effect=IOError("Mock IOError")):
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            # Вызываем тестируемую функцию и проверяем результат
            result = get_transactions_csv("dummy_path.csv")
            assert result == []
            mock_logger.error.assert_called_once_with("Unexpected error: Mock IOError")


# Тест на отсутствие файла
def test_get_transactions_excel_file_not_found():
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = False
        result = get_transactions_excel("nonexistent_file.xlsx")
        assert result == []


# Тест на неверный формат файла
def test_get_transactions_excel_invalid_file_format():
    with patch("openpyxl.load_workbook") as mock_load_workbook:
        mock_load_workbook.side_effect = openpyxl.utils.exceptions.InvalidFileException
        result = get_transactions_excel("invalid_format.xlsx")
        assert result == []


# Тест на пустой файл
def test_get_transactions_excel_empty_file():
    with patch("openpyxl.load_workbook") as mock_load_workbook:
        mock_sheet = mock_load_workbook().active
        mock_sheet.iter_rows.return_value = []
        result = get_transactions_excel("empty_file.xlsx")
        assert result == []


def test_get_greeting():
    assert get_greeting("2024-07-16 18:38:44.341897") == "Добрый вечер"
    assert get_greeting("2024-07-16 00:38:44.341897") == "Доброй ночи"
    assert get_greeting("2024-07-16 07:38:44.341897") == "Доброе утро"
    assert get_greeting("2024-07-16 14:38:44.341897") == "Добрый день"


def test_get_card_number_list(transaction2):
    assert get_card_number_list(transaction2) == ["*7197", "*4556"]


def test_get_operations_sum(transaction2):
    assert get_operations_sum("2019-09-30", transaction2, "*7197") == 678.77
    assert get_operations_sum("2019-09-30", transaction2, "*4556") == 0


@pytest.mark.parametrize(
    "x, expected", [(1056.45, 10.56), (9387.67, 93.88), (334.34, 3.34)]
)
def test_get_cashback_sum(x, expected):
    assert get_cashback_sum(x) == expected


def test_show_cards(transaction2):
    assert show_cards("2019-09-30", transaction2) == [
        {"last_digits": "7197", "total_spent": 678.77, "cashback": 6.79},
        {"last_digits": "4556", "total_spent": 0, "cashback": 0.0},
    ]


def test_show_top_5_transactions(transaction2):
    assert show_top_5_transactions("2019-09-30", transaction2) == [
        {
            "date": "27.09.2019",
            "amount": 1000.0,
            "category": "Бонусы",
            "description": 'Пополнение. Тинькофф Банк. Бонус по акции "Приведи друга"',
        },
        {
            "date": "27.09.2019",
            "amount": 357.22,
            "category": "Отели",
            "description": "Dongying Luxury Blue Hori",
        },
        {
            "date": "26.09.2019",
            "amount": 250.0,
            "category": "Пополнения",
            "description": "Пополнение через Альфа-Банк",
        },
        {
            "date": "28.09.2019",
            "amount": 177.1,
            "category": "Супермаркеты",
            "description": "SPAR",
        },
        {
            "date": "29.09.2019",
            "amount": 144.45,
            "category": "Супермаркеты",
            "description": "Колхоз",
        },
    ]


@patch("requests.get")
def test_fetch_and_show_currency_rates(mock_get):
    mock_get.return_value.json.return_value = (
    {'Date': '2024-07-20T11:30:00+03:00', 'PreviousDate': '2024-07-19T11:30:00+03:00',
     'PreviousURL': '//www.cbr-xml-daily.ru/archive/2024/07/19/daily_json.js', 'Timestamp': '2024-07-21T16:00:00+03:00',
     'Valute': {
         'AUD': {'ID': 'R01010', 'NumCode': '036', 'CharCode': 'AUD', 'Nominal': 1, 'Name': 'Австралийский доллар',
                 'Value': 58.9826, 'Previous': 59.2192},
         'AZN': {'ID': 'R01020A', 'NumCode': '944', 'CharCode': 'AZN', 'Nominal': 1, 'Name': 'Азербайджанский манат',
                 'Value': 51.7768, 'Previous': 51.6914},
         'GBP': {'ID': 'R01035', 'NumCode': '826', 'CharCode': 'GBP', 'Nominal': 1,
                 'Name': 'Фунт стерлингов Соединенного королевства', 'Value': 114.2331, 'Previous': 114.361},
         'AMD': {'ID': 'R01060', 'NumCode': '051', 'CharCode': 'AMD', 'Nominal': 100, 'Name': 'Армянских драмов',
                 'Value': 22.6641, 'Previous': 22.6489},
         'BYN': {'ID': 'R01090B', 'NumCode': '933', 'CharCode': 'BYN', 'Nominal': 1, 'Name': 'Белорусский рубль',
                 'Value': 27.758, 'Previous': 27.6607},
         'BGN': {'ID': 'R01100', 'NumCode': '975', 'CharCode': 'BGN', 'Nominal': 1, 'Name': 'Болгарский лев',
                 'Value': 49.1897, 'Previous': 49.1264},
         'BRL': {'ID': 'R01115', 'NumCode': '986', 'CharCode': 'BRL', 'Nominal': 1, 'Name': 'Бразильский реал',
                 'Value': 15.8816, 'Previous': 16.0747},
         'HUF': {'ID': 'R01135', 'NumCode': '348', 'CharCode': 'HUF', 'Nominal': 100, 'Name': 'Венгерских форинтов',
                 'Value': 24.4835, 'Previous': 24.6274},
         'VND': {'ID': 'R01150', 'NumCode': '704', 'CharCode': 'VND', 'Nominal': 10000, 'Name': 'Вьетнамских донгов',
                 'Value': 36.3031, 'Previous': 36.2358},
         'HKD': {'ID': 'R01200', 'NumCode': '344', 'CharCode': 'HKD', 'Nominal': 1, 'Name': 'Гонконгский доллар',
                 'Value': 11.2905, 'Previous': 11.2733},
         'GEL': {'ID': 'R01210', 'NumCode': '981', 'CharCode': 'GEL', 'Nominal': 1, 'Name': 'Грузинский лари',
                 'Value': 32.6571, 'Previous': 32.5766},
         'DKK': {'ID': 'R01215', 'NumCode': '208', 'CharCode': 'DKK', 'Nominal': 1, 'Name': 'Датская крона',
                 'Value': 12.8958, 'Previous': 12.8806},
         'AED': {'ID': 'R01230', 'NumCode': '784', 'CharCode': 'AED', 'Nominal': 1, 'Name': 'Дирхам ОАЭ',
                 'Value': 23.9675, 'Previous': 23.928},
         'USD': {'ID': 'R01235', 'NumCode': '840', 'CharCode': 'USD', 'Nominal': 1, 'Name': 'Доллар США',
                 'Value': 88.0206, 'Previous': 87.8754},
         'EUR': {'ID': 'R01239', 'NumCode': '978', 'CharCode': 'EUR', 'Nominal': 1, 'Name': 'Евро', 'Value': 96.0371,
                 'Previous': 96.1018},
         'EGP': {'ID': 'R01240', 'NumCode': '818', 'CharCode': 'EGP', 'Nominal': 10, 'Name': 'Египетских фунтов',
                 'Value': 18.242, 'Previous': 18.2119},
         'INR': {'ID': 'R01270', 'NumCode': '356', 'CharCode': 'INR', 'Nominal': 10, 'Name': 'Индийских рупий',
                 'Value': 10.5237, 'Previous': 10.5065},
         'IDR': {'ID': 'R01280', 'NumCode': '360', 'CharCode': 'IDR', 'Nominal': 10000, 'Name': 'Индонезийских рупий',
                 'Value': 54.4682, 'Previous': 54.4829},
         'KZT': {'ID': 'R01335', 'NumCode': '398', 'CharCode': 'KZT', 'Nominal': 100, 'Name': 'Казахстанских тенге',
                 'Value': 18.4518, 'Previous': 18.5067},
         'CAD': {'ID': 'R01350', 'NumCode': '124', 'CharCode': 'CAD', 'Nominal': 1, 'Name': 'Канадский доллар',
                 'Value': 64.2674, 'Previous': 64.2129},
         'QAR': {'ID': 'R01355', 'NumCode': '634', 'CharCode': 'QAR', 'Nominal': 1, 'Name': 'Катарский риал',
                 'Value': 24.1815, 'Previous': 24.1416},
         'KGS': {'ID': 'R01370', 'NumCode': '417', 'CharCode': 'KGS', 'Nominal': 10, 'Name': 'Киргизских сомов',
                 'Value': 10.3991, 'Previous': 10.3624},
         'CNY': {'ID': 'R01375', 'NumCode': '156', 'CharCode': 'CNY', 'Nominal': 1, 'Name': 'Китайский юань',
                 'Value': 12.0335, 'Previous': 12.0227},
         'MDL': {'ID': 'R01500', 'NumCode': '498', 'CharCode': 'MDL', 'Nominal': 10, 'Name': 'Молдавских леев',
                 'Value': 49.7019, 'Previous': 49.5986},
         'NZD': {'ID': 'R01530', 'NumCode': '554', 'CharCode': 'NZD', 'Nominal': 1, 'Name': 'Новозеландский доллар',
                 'Value': 53.0544, 'Previous': 53.3535},
         'NOK': {'ID': 'R01535', 'NumCode': '578', 'CharCode': 'NOK', 'Nominal': 10, 'Name': 'Норвежских крон',
                 'Value': 81.8918, 'Previous': 81.7202},
         'PLN': {'ID': 'R01565', 'NumCode': '985', 'CharCode': 'PLN', 'Nominal': 1, 'Name': 'Польский злотый',
                 'Value': 22.3057, 'Previous': 22.3624},
         'RON': {'ID': 'R01585F', 'NumCode': '946', 'CharCode': 'RON', 'Nominal': 1, 'Name': 'Румынский лей',
                 'Value': 19.2732, 'Previous': 19.3269},
         'XDR': {'ID': 'R01589', 'NumCode': '960', 'CharCode': 'XDR', 'Nominal': 1,
                 'Name': 'СДР (специальные права заимствования)', 'Value': 116.9855, 'Previous': 116.7978},
         'SGD': {'ID': 'R01625', 'NumCode': '702', 'CharCode': 'SGD', 'Nominal': 1, 'Name': 'Сингапурский доллар',
                 'Value': 65.4818, 'Previous': 65.5346},
         'TJS': {'ID': 'R01670', 'NumCode': '972', 'CharCode': 'TJS', 'Nominal': 10, 'Name': 'Таджикских сомони',
                 'Value': 82.5818, 'Previous': 82.4455},
         'THB': {'ID': 'R01675', 'NumCode': '764', 'CharCode': 'THB', 'Nominal': 10, 'Name': 'Таиландских батов',
                 'Value': 24.2963, 'Previous': 24.4356},
         'TRY': {'ID': 'R01700J', 'NumCode': '949', 'CharCode': 'TRY', 'Nominal': 10, 'Name': 'Турецких лир',
                 'Value': 26.6175, 'Previous': 26.5744},
         'TMT': {'ID': 'R01710A', 'NumCode': '934', 'CharCode': 'TMT', 'Nominal': 1, 'Name': 'Новый туркменский манат',
                 'Value': 25.1487, 'Previous': 25.1073},
         'UZS': {'ID': 'R01717', 'NumCode': '860', 'CharCode': 'UZS', 'Nominal': 10000, 'Name': 'Узбекских сумов',
                 'Value': 69.8516, 'Previous': 69.8092},
         'UAH': {'ID': 'R01720', 'NumCode': '980', 'CharCode': 'UAH', 'Nominal': 10, 'Name': 'Украинских гривен',
                 'Value': 21.2497, 'Previous': 21.1938},
         'CZK': {'ID': 'R01760', 'NumCode': '203', 'CharCode': 'CZK', 'Nominal': 10, 'Name': 'Чешских крон',
                 'Value': 37.9481, 'Previous': 37.9903},
         'SEK': {'ID': 'R01770', 'NumCode': '752', 'CharCode': 'SEK', 'Nominal': 10, 'Name': 'Шведских крон',
                 'Value': 83.4127, 'Previous': 83.4887},
         'CHF': {'ID': 'R01775', 'NumCode': '756', 'CharCode': 'CHF', 'Nominal': 1, 'Name': 'Швейцарский франк',
                 'Value': 99.0665, 'Previous': 99.3616},
         'RSD': {'ID': 'R01805F', 'NumCode': '941', 'CharCode': 'RSD', 'Nominal': 100, 'Name': 'Сербских динаров',
                 'Value': 81.8728, 'Previous': 82.1007},
         'ZAR': {'ID': 'R01810', 'NumCode': '710', 'CharCode': 'ZAR', 'Nominal': 10, 'Name': 'Южноафриканских рэндов',
                 'Value': 47.9676, 'Previous': 48.3469},
         'KRW': {'ID': 'R01815', 'NumCode': '410', 'CharCode': 'KRW', 'Nominal': 1000, 'Name': 'Вон Республики Корея',
                 'Value': 63.7877, 'Previous': 63.6087},
         'JPY': {'ID': 'R01820', 'NumCode': '392', 'CharCode': 'JPY', 'Nominal': 100, 'Name': 'Японских иен',
                 'Value': 55.9287, 'Previous': 56.4208}}})
    assert fetch_and_show_currency_rates() == [{'currency': 'USD', 'rate': 88.02}, {'currency': 'EUR', 'rate': 96.04}]
    mock_get.assert_called_once_with(
        "https://www.cbr-xml-daily.ru/daily_json.js", headers={"apikey": api_key})