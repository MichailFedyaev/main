# `Banking operations widget`

Программа скрывает номер карты и счета, а также фильтрует и сортирует банковские счета по дате и оплате.

## Project dependencies:
- The program uses the version Python 3.12
- flake8 = "7.0.0"
- black = "24.4.2"
- isort = "5.13.2"
- mypy = "1.10.0"
- pytest = "^8.2.2"
- pytest-cov = "^5.0.0"

## Функции, которые мы будем использовать в этой версии кода:

- Функция скрывающая номер карты и счета
- Функция сортировки по дате
- Функция фильтрации в операциях по счетам

## Структура проекта
Был добавлен pytest, для запуска тестов и проверки функций, а также pytest-cov, для анализа покрытия кода тестами
Была добавлена папка (htmlcov) с отчетом покрытия тестами в формате HTML.
Тесты функционала с помощью pytest-cov:

---------- coverage: platform win32, python 3.12.1-final-0 ----------- 
Name                             Stmts   Miss  Cover
----------------------------------------------------
src\__init__.py                      0      0   100%
src\masks.py                        10      1    90%
src\processing.py                   13      0   100%
src\widget.py                       15      0   100%
tests\__init__.py                    0      0   100%
tests\conftest.py                   11      0   100%
tests\test_masks_and_widget.py      14      0   100%
tests\test_processing.py             7      0   100%
----------------------------------------------------
TOTAL                               70      1    99%

# Инструкция по установке
Чтобы скачать репозиторий:

`git clone git@github.com:MichailFedyaev/main.git`

Затем вам необходимо установить основные зависимости для запуска проекта в вашей системе:

```pip install -r requirements.txt```

## Контакт для обратной связи
За дополнительной информацией обращаться: `drovosekov1910@mail.ru`