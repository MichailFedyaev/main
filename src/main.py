from src.utils import get_transactions_dictionary, get_transactions_csv, get_transactions_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, search_transactions, sort_by_date
from src.widget import get_data, mask_account_card


def main() -> None:
    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла"""
    )

    while True:
        selected_format = input("\nВаш выбор: ").strip().lower()
        if selected_format == "1":
            print("\nДля обработки выбран JSON-файл.")
            transactions = get_transactions_dictionary("D:/PycharmProject/main/data/operations.json")
            break
        elif selected_format == "2":
            print("\nДля обработки выбран CSV-файл.")
            transactions = get_transactions_csv("D:/PycharmProject/main/data/transactions.csv")
            break
        elif selected_format == "3":
            print("\nДля обработки выбран XLSX-файл.")
            transactions = get_transactions_excel("D:/PycharmProject/main/data/transactions_excel.xlsx")
            break
        else:
            print("\nВы ввели неверное значение. Пожалуйста, выберите номер пункта из меню.")

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        selected_state = input("\nСтатус: ").strip().upper()
        if selected_state == "EXECUTED":
            user_transactions = filter_by_state(transactions)
            print('\nОперации отфильтрованы по статусу "EXECUTED"')
            break
        elif selected_state == "CANCELED":
            user_transactions = filter_by_state(transactions, "CANCELED")
            print('\nОперации отфильтрованы по статусу "CANCELED"')
            break
        elif selected_state == "PENDING":
            user_transactions = filter_by_state(transactions, "PENDING")
            print('\nОперации отфильтрованы по статусу "PENDING"')
            break
        else:
            print(f'Статус операции "{selected_state}" недоступен.')

    need_to_sort_by_date = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()
    while True:
        if need_to_sort_by_date in {"да", "нет"}:
            break
        else:
            need_to_sort_by_date = (
                input(
                    f"{need_to_sort_by_date} \
            - неизвестный ответ, введите Да или Нет: "
                )
                .strip()
                .lower()
            )

    if need_to_sort_by_date == "да":
        print("\nОтсортировать по возрастанию или по убыванию?")
        while True:
            ascending = input("Сортировка: ").strip().lower()
            if ascending == "по возрастанию":
                user_transactions = sort_by_date(user_transactions)
                break
            elif ascending == "по убыванию":
                user_transactions = sort_by_date(user_transactions, False)
                break
            else:
                print(f"{ascending} - неизвестный ответ, сортировать можно по возрастанию/по убыванию.")

    need_to_filter_by_currency = input("\nВыводить только рублевые тразакции? Да/Нет: ").strip().lower()
    while True:
        if need_to_filter_by_currency == "да":
            user_transactions = list(filter_by_currency(user_transactions, "RUB"))
            break
        elif need_to_filter_by_currency == "нет":
            break
        else:
            need_to_filter_by_currency = (
                input(
                    f"{need_to_filter_by_currency} \
            - неизвестный ответ, введите Да или Нет: "
                )
                .strip()
                .lower()
            )

    print("\nОтфильтровать список транзакций по определенному слову в описании?")
    need_to_search = input("Да/Нет: ").strip().lower()
    while True:
        if need_to_search == "да":
            search_string = input("\nПо какому слову в описании будем фильтровать транзакции?: ")
            user_transactions = search_transactions(user_transactions, search_string)
            break
        elif need_to_search == "нет":
            break
        else:
            need_to_search = input(f"{need_to_search} - неизвестный ответ, введите Да или Нет: ")

    if not user_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print("\nВсего банковских операций в выборке:", len(list(user_transactions)))

    for transaction in transactions:
        print()
        date_str = transaction.get("date", "")
        if date_str:
            date = get_data(date_str)
        description = transaction.get("description", "")
        print(date, description)

        from_card_or_account = transaction.get("from", "")
        to_card_or_account = transaction.get("to", "")
        to_masked_card_or_account = mask_account_card(to_card_or_account)
        if from_card_or_account:
            from_masked_card_or_account = mask_account_card(from_card_or_account)
            print(from_masked_card_or_account, "->", to_masked_card_or_account)
        else:
            print(to_masked_card_or_account)

        amount = transaction.get("operationAmount")
        if amount:
            currency = amount.get("currency", {}).get("code", "")
            amount = amount.get("amount")
        else:
            amount = transaction.get("amount")
            currency = transaction.get("currency_name", "")
        print("Сумма", amount, currency)


if __name__ == "__main__":
    main()