import telebot
import name_rates
import all_rates

from config import token
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup



# States storage
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(token,
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

@bot.message_handler(commands=['name_rates'])
def print_names_rates(message):
    strings_names = []
    for key, item in name_rates.get_name_rates().items():
        strings_names.append("{}: {}".format(key.capitalize(), item))
    result = "; \n".join(strings_names)

    bot.send_message(message.chat.id, f"""*Допустимые валюты и их расшифровка* 
{result}""", parse_mode="Markdown")

@bot.message_handler(commands=['get_rates'])
def send_rates(message):
    binance_rate = all_rates.get_binance_rates()
    garantex_rate = all_rates.get_garantex_rates()
    all_rates.get_other_rates()
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
    bot.set_state(message.from_user.id, MyStates.eur, message.chat.id)
    bot.send_message(message.chat.id, 'Сколько евро у вас есть?')


@bot.message_handler(state=MyStates.eur, is_digit=True)
def get_message(message):
    """
    State 1. Will process when user's state is MyStates.eur
    """

    result = f"{message.text} евро, это " + '{:.2f}'.format(
    float(all_rates.get_fixer_rates()) * int(message.text)) + " в рублях"
    bot.send_message(message.chat.id, result, parse_mode="html")

    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.eur, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for MyStates.eur
    """
    bot.send_message(message.chat.id,
                     'Похоже, вы отправляете строку. Пожалуйста, введите цифру. Сколько евро у вас есть?')


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())
    bot.infinity_polling(skip_pending=True)
