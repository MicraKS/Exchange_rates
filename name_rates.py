import requests

def get_name_rates():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url=url).json()
    data = {}
    for key, value in response['Valute'].items():
        for key_value,value_value in value.items():
            if key_value == "Name":
                data[key] = value_value
    return data
