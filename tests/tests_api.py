import pytest

import requests
import main



def test_url(requests_mock):
    requests_mock.get('https://cloud.iexapis.com/v1', text='data')
    assert 'data' == requests.get('https://cloud.iexapis.com/v1').text


def test_load_data_from_csv():
    test_csv=main.Stocks()

    assert "... Data Loaded" == test_csv.load_data_from_csv()

def test_connection():
    test_connect2=main.Stocks()

    assert "... Error in connecting" == test_connect2.refresh_live_stock_price()

def test_json_conversion():
    test_json=main.Stocks()

    with pytest.raises(AttributeError):
        test_json.convert_data()


def test_writing():
    test_data=main.Stocks()

    with pytest.raises(AttributeError):
        test_data.write_data()
