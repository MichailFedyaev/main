from datetime import datetime
from typing import Any

from src.masks import mask_account, mask_card_number


def mask_account_card(string: str) -> Any:
    if "Счет" in string:
        account = string[5:]
        return "Счет" + " " + mask_account(account)
    else:
        card_number = "".join(string[-16:].split())
        return string[:-16] + mask_card_number(card_number)


def get_data(data: str) -> str:
    time = datetime.strptime(data, format("%Y-%m-%dT%H:%M:%S.%f"))
    return time.strftime("%d.%m.%Y")


print(mask_account_card("Счет 73654108430135874305"))
print(mask_account_card("MasterCard 7158300734726759"))
print(get_data("2018-07-11T02:26:18.671407"))
