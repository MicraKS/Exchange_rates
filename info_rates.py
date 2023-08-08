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

def get_price_rates(listKey):
    for key, value in response_rates.items():
        if key == listKey[0]:
            print(key)
            print(listKey)
            listKey.clear()
            break