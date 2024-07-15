import pytest
from src.external_api import convert_to_rub

from unittest.mock import patch


@patch('requests.get')
def test_convert_to_rub(mock_get):
    mock_get.return_value.json.return_value = {"result": 43698.21}
    mock_get.return_value.status_code = 200
    assert convert_to_rub(500, "USD") == 43698.21
    mock_get.assert_called_once_with("https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=500", headers={'apikey': '2yXsr7OFQ4LdCOi7stZxAKP4RjyVI4Q2'})
