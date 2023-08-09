import requests


def get_binance_rates():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    headers = {
        'assept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36',
    }
    params = {"fiat": "RUB",
              "page": 1,
              "rows": 10,
              "tradeType": "BUY",
              "asset": "USDT",
              "countries": [],
              "proMerchantAds": False,
              "shieldMerchantAds": False,
              "publisherType": None,
              "payTypes": ["TinkoffNew"],
              }
    response = requests.post(url, headers=headers, json=params).json()
    return response['data'][0]['adv']['price']


def get_garantex_rates():
    url = 'https://garantex.io/api/v2/depth?market=usdtrub'
    response = requests.get(url=url).json()
    return response['asks'][0]['price']


def get_fixer_rates():
    url = 'http://data.fixer.io/api/latest?access_key=d24c65ca6d0029ae972001e5b5d075fe&symbols=RUB'
    response = requests.get(url=url).json()
    return '{:.2f}'.format(response['rates']['RUB'])


def get_other_rates():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    url_price = 'https://www.cbr-xml-daily.ru/latest.js'
    response = requests.get(url=url).json()
    response_price = requests.get(url=url_price).json()
    return response['Valute'], response_price['rates']
