import requests

url = 'https://www.cbr-xml-daily.ru/daily_json.js'
response = requests.get(url=url).json()


def get_name_rates():
    strings_names = []
    for key, value in response['Valute'].items():
        for key_value, value_value in value.items():
            if key_value == "Name":
                strings_names.append("{}: {}".format(key, value_value))
    return "; \n".join(strings_names)
