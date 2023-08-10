import telebot
import os
import info_rates
import all_rates

from dotenv import load_dotenv
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup

# States storage
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()

load_dotenv()
bot = telebot.TeleBot(os.getenv('token'),
                      state_storage=state_storage)
valute_names, valute_key = info_rates.get_name_rates()
listKey = []


# States group.
class MyStates(StatesGroup):
    valute = State()
    converter = State()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """Привет!

С помощью этого боты ты сможешь узнавать курсы USDT на следующих биржах:
-Binance P2P Тинькофф
-Garantex
А также узнать курс рубля к другим валютам""")


@bot.message_handler(commands=['name_rates'])
def print_names_rates(message):
    bot.send_message(message.chat.id, f"""*Допустимые валюты и их расшифровка* 
{valute_names}""", parse_mode="Markdown")


@bot.message_handler(commands=['get_rates'])
def send_rates(message):
    binance_rate = all_rates.get_binance_rates()
    garantex_rate = all_rates.get_garantex_rates()
    bot.send_message(message.chat.id, f"""Курсы валют
-Binance Tinkoff {binance_rate}
-Garantex {garantex_rate}""")


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['get_eur'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.valute, message.chat.id)
    bot.send_message(message.chat.id, 'Какая валюта интересует? Введите аббревиатуру')


@bot.message_handler(state=MyStates.valute, func=lambda msg: msg.text.upper() in valute_key)
def get_message(message):
    input_currency = message.text.upper()
    append_in_listkey(msg=input_currency)

    bot.set_state(message.from_user.id, MyStates.converter, message.chat.id)
    bot.send_message(message.chat.id, 'Сколько рублей будем переводить')


@bot.message_handler(state=MyStates.valute)
def age_incorrect(message):
    bot.set_state(message.from_user.id, MyStates.valute, message.chat.id)
    bot.send_message(message.chat.id,
                     'Что-то пошло не так. Введите аббревиатуру нужной валюты')


@bot.message_handler(state=MyStates.converter, is_digit=True)
def get_digit(message):
    append_in_listkey(msg=message.text)
    result = info_rates.get_price_rates(listKey)

    bot.send_message(message.chat.id, result)
    bot.delete_state(message.from_user.id, message.chat.id)


#
#
@bot.message_handler(state=MyStates.converter, is_digit=False)
def digit_incorrect(message):
    bot.send_message(message.chat.id,
                     'Похоже, вы отправляете строку. Пожалуйста, введите цифру.')


def append_in_listkey(msg):
    listKey.append(msg)


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())
    bot.infinity_polling(skip_pending=True)
