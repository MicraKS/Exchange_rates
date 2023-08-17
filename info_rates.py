import all_rates

response_valute, response_rates = all_rates.get_other_rates()


def get_name_rates():
    strings_names = []
    valute_key = []
    for key, value in response_valute.items():
        for key_value, value_value in value.items():
            if key_value == "Name":
                strings_names.append("{}: {}".format(key, value_value))
                valute_key.append(key)
    return "; \n".join(strings_names), valute_key


def get_price_rates(listkey):
    for key, value in response_rates.items():
        if key == listkey[0]:
            result = int(listkey[1]) * value
            print(result)
            listkey.clear()
            return result

def get_value_all_rates():
    valute, price_rates = all_rates.get_other_rates()
    list_valute = []
    for i, g in valute.items():
        list_valute.append(f"{g['Name']} {round(g['Value']/g['Nominal'], 3)}")

    return "; \n".join(list_valute)
