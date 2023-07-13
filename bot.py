import telebot
import requests

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup

# States storage
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()

bot = telebot.TeleBot("5463016829:AAGpcnSPd8nCyG0e1eMO5AZbE5gsKHnxZQo",
                      state_storage=state_storage)


# States group.
class MyStates(StatesGroup):
    eur = State()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """Привет!

С помощью этого боты ты сможешь узнавать курсы USDT на следующих биржах:
-Binance P2P Тинькофф
-Garantex
А также узнать курс EUR""")


@bot.message_handler(commands=['get_rates'])
def send_rates(message):
    binance_rate = get_binance_rates()
    garantex_rate = get_garantex_rates()
    bot.send_message(message.chat.id, f"""Курсы валют
-Binance Tinkoff {binance_rate}
-Garantex {garantex_rate}""")


def get_binance_rates():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    headers = {
        'assept' : '*/*',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    params = {"fiat" : "RUB",
               "page" : 1,
              "rows" : 10,
              "tradeType" : "BUY",
              "asset" : "USDT",
              "countries" : [],
              "proMerchantAds" : False,
              "shieldMerchantAds" : False,
              "publisherType" : None,
              "payTypes" : ["TinkoffNew"],
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
# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(commands=['get_message'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.eur, message.chat.id)
    bot.send_message(message.chat.id, 'Сколько евро у вас есть?')

@bot.message_handler(state=MyStates.eur, is_digit=True)
def get_message(message):
    """
    State 1. Will process when user's state is MyStates.eur
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        result = f"{message.text} евро, это "+ '{:.2f}'.format(float(get_fixer_rates()) * int(message.text))+ " в рублях"
        bot.send_message(message.chat.id, result, parse_mode="html")

    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(state=MyStates.eur, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for MyStates.eur
    """
    bot.send_message(message.chat.id, 'Похоже, вы отправляете строку. Пожалуйста, введите цифру. Сколько евро у вас есть?')


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())
    bot.infinity_polling(skip_pending=True)