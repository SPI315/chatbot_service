import os
import sys
import json
import time
import telebot
from telebot import types

from dotenv import load_dotenv

import requests

from database.database import SessionLocal



env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)

bot = telebot.TeleBot(token=os.getenv("TG_TOKEN"))
session = SessionLocal()

FASTAPI_URL = os.getenv("FASTAPI_URL")

# инициация бота
@bot.message_handler(commands=["start"])
def startBot(message):
    first_mess = "Тебя приветствует мощнейший искусственный интеллект!\nВойди или зарегистрируйся:"
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    button_reg = types.InlineKeyboardButton(text="Регистриция", callback_data="reg")
    button_auth = types.InlineKeyboardButton(text="Авторизация", callback_data="auth")
    markup.add(button_reg, button_auth)
    bot.send_message(chat_id, first_mess, parse_mode="html", reply_markup=markup)
    bot.edit_message_reply_markup(
        chat_id=chat_id, message_id=message.message_id, reply_markup=None
    )


# авторизация пользователя
@bot.callback_query_handler(func=lambda call: call.data == "auth")
def auth_init(call_auth):
    message = call_auth.message
    chat_id = message.chat.id
    markup = types.ForceReply()
    bot.send_message(chat_id, "Какой у тебя email?", reply_markup=markup)
    bot.register_next_step_handler(message, email_auth)


def email_auth(message):
    chat_id = message.chat.id
    markup = types.ForceReply()
    email = message.text
    bot.send_message(chat_id, "А пароль?", reply_markup=markup)
    bot.register_next_step_handler(message, passw_auth, email)


def passw_auth(message, email):
    chat_id = message.chat.id
    user_password = message.text
    data = {"username": email, "password": user_password}
    response = requests.post(f"{FASTAPI_URL}/user/signin/", data=data)
    if result != "Все верно. Доступ открыт":
        bot.send_message(chat_id, result)
        startBot(message)
    else:
        user = User().get_user_by_email(session=session, email=email)
        bot.send_message(chat_id, result)
        user_id = user.id
        user_menu(message, user_id)


# основное меню (показывается после авторизации)
def user_menu(message, user_id):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    button_hist_load = types.InlineKeyboardButton(
        text="Загрузить историю транзакций", callback_data=f"hist_load/{user_id}"
    )
    button_hist_data = types.InlineKeyboardButton(
        text="Загрузить историю запросов", callback_data=f"hist_data/{user_id}"
    )
    button_repl = types.InlineKeyboardButton(
        text="Пополнить баланс", callback_data=f"repl/{user_id}"
    )
    button_balance = types.InlineKeyboardButton(
        text="Проверить баланс", callback_data=f"balance/{user_id}"
    )
    button_pred = types.InlineKeyboardButton(
        text="Узнать что-нибудь", callback_data=f"pred/{user_id}"
    )
    button_start = types.InlineKeyboardButton(
        text="Начать сначала", callback_data="start"
    )
    markup.add(button_hist_load, button_hist_data)
    markup.add(button_repl, button_balance)
    markup.add(button_pred)
    markup.add(button_start)
    bot.send_message(chat_id, "Чем теперь займемся?", reply_markup=markup)
    bot.edit_message_reply_markup(
        chat_id=chat_id, message_id=message.message_id, reply_markup=None
    )


# возврат к регистрации и авторизации
@bot.callback_query_handler(func=lambda call: call.data == "start")
def start_over(call):
    message = call.message
    startBot(message)


# цепочка для регистрация пользователя
@bot.callback_query_handler(func=lambda call: call.data == "reg")
def reg_init(call_reg):
    message = call_reg.message
    chat_id = message.chat.id
    markup = types.ForceReply()
    bot.send_message(
        chat_id,
        "Сейчас мы тебя запишем.\nКакой у тебя email?",
        parse_mode="html",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, email_reg)


def email_reg(message):

    chat_id = message.chat.id
    markup = types.ForceReply()
    user_data = {}
    user_data["email"] = message.text
    bot.send_message(
        chat_id,
        "Окееееей))\nТеперь придумай пароль.",
        parse_mode="html",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, passw_reg, user_data)


def passw_reg(message, user_data):

    chat_id = message.chat.id
    markup = types.ForceReply()
    bot.send_message(
        chat_id,
        "Отлично!\nА как тебя зовут?",
        parse_mode="html",
        reply_markup=markup,
    )
    user_data["password"] = message.text  # TODO добавить хэширование
    bot.register_next_step_handler(message, name_reg, user_data)


def name_reg(message, user_data):
    chat_id = message.chat.id
    markup = types.ForceReply()
    bot.send_message(
        chat_id,
        f"{message.text}, ты супер!\nЕще подскажи фамилию.",
        parse_mode="html",
        reply_markup=markup,
    )
    user_data["name"] = message.text
    bot.register_next_step_handler(message, surname_reg, user_data)


def surname_reg(message, user_data):
    chat_id = message.chat.id
    markup = types.ForceReply()
    bot.send_message(
        chat_id,
        f"Значит, ты {user_data['name']} {message.text}...\nА номер телефона у тебя какой?",
        parse_mode="html",
        reply_markup=markup,
    )
    user_data["surname"] = message.text
    bot.register_next_step_handler(message, phone_reg, user_data)


def phone_reg(message, user_data):
    chat_id = message.chat.id
    user_data["phone"] = message.text
    user = User(
        email=user_data["email"],
        phone=user_data["phone"],
        user_name=user_data["name"],
        user_surname=user_data["surname"],
        user_password=user_data["password"],
        tg_id=message.from_user.id,
    )
    user.user_add(session=session)
    name = user_data["name"]
    markup = types.InlineKeyboardMarkup()
    button_auth = types.InlineKeyboardButton(text="Авторизация", callback_data="auth")
    markup.add(button_auth)
    bot.send_message(
        chat_id, f"А теперь, {name}, давай ка авторизуемся!", reply_markup=markup
    )
    bot.edit_message_text(
        text="Авторизуемся....", chat_id=chat_id, message_id=message.id
    )


# загрузка истории транзакций
@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_load"))
def hist_load(call):
    message = call.message
    chat_id = message.chat.id
    data_parts = call.data.split("/")
    if len(data_parts) == 2 and data_parts[0] == "hist_load":
        user_id = data_parts[1]
        transaction = Transaction()
        hist = transaction.load_history(session=session, user_id=user_id)
        if hist:
            hist = transaction.transform_history(hist)
            for key in hist.keys():
                bot.send_message(chat_id, f"{key}: {hist[key]}")
        else:
            bot.send_message(chat_id, "Нет истории - нет проблем.")
        user_menu(message, user_id)
    else:
        bot.send_message(chat_id, "Извини, но я прилег.\nПопробуй позже.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_data"))
def hist_data(call):
    message = call.message
    chat_id = message.chat.id
    data_parts = call.data.split("/")
    if len(data_parts) == 2 and data_parts[0] == "hist_data":
        user_id = data_parts[1]
        data_hist = OperData().load_data(session=session, user_id=user_id)
        
        if data_hist:
            data_hist = OperData().transform_data(data_hist)
            for key in data_hist.keys():
                bot.send_message(chat_id, f"{key}: {data_hist[key]}")
        else:
            bot.send_message(chat_id, "Нет истории - нет проблем.")
        user_menu(message, user_id)
    else:
        bot.send_message(chat_id, "Извини, но я прилег.\nПопробуй позже.")


# удаление истории транзакций
@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_del"))
def hist_del(call):
    message = call.message
    chat_id = message.chat.id
    data_parts = call.data.split("/")
    if len(data_parts) == 2 and data_parts[0] == "hist_del":
        user_id = data_parts[1]
        transaction = Transaction()
        transaction.del_history(session=session, user_id=user_id)
        bot.send_message(chat_id, "История транзакций удалена.")
        user_menu(message, user_id)
    else:
        bot.send_message(chat_id, "Извини, но я прилег.\nПопробуй позже.")


# пополнение баланса
@bot.callback_query_handler(func=lambda call: call.data.startswith("repl"))
def repl_init(call):
    message = call.message
    chat_id = message.chat.id
    data_parts = call.data.split("/")
    if len(data_parts) == 2 and data_parts[0] == "repl":
        user_id = data_parts[1]
        markup = types.ForceReply()
        bot.send_message(
            chat_id, "Сколько денег ты хочешь потратить?", reply_markup=markup
        )
        bot.register_next_step_handler(message, repl, user_id)
    else:
        bot.send_message(chat_id, "Извини, но я прилег.\nПопробуй позже.")


def repl(message, user_id):
    chat_id = message.chat.id
    try:
        value = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "Для пополнения баланса введи целое число.")
        bot.register_next_step_handler(message, repl, user_id)

    transaction = Transaction()
    transaction.replanishment(session=session, user_id=user_id, value=value)
    bot.send_message(chat_id, "Баланс пополнен.")
    user_menu(message, user_id)


# предсказание
@bot.callback_query_handler(func=lambda call: call.data.startswith("pred"))
def pred_init(call):
    message = call.message
    chat_id = message.chat.id
    data_parts = call.data.split("/")
    if len(data_parts) == 2 and data_parts[0] == "pred":
        user_id = data_parts[1]
        user = User(user_id=user_id)
        if user.check_balance(session=session) < 100:
            bot.send_message(chat_id, "Кинь сотку на баланс.")
            user_menu(message, user_id)
        else:
            markup = types.ForceReply()
            bot.send_message(chat_id, "Начни фразу, а я продолжу.", reply_markup=markup)
            bot.register_next_step_handler(message, pred, user_id)
    else:
        bot.send_message(chat_id, "Извини, но я прилег.\nПопробуй позже.")


def pred(message, user_id):
    chat_id = message.chat.id
    data = message.text
    to_send = json.dumps({user_id: data})
    send_message(message=to_send)
    bot.send_message(chat_id, "Запрос отправлен в очередь. Скоро вернусь.")
    save_data(message, user_id, data)


def save_data(message, user_id, input_data):
    data = OperData(input_data, user_id)
    data.save_input_data(session=session)
    callback(message, user_id, data)


def callback(message, user_id, data):
    chat_id = message.chat.id
    if data.check_output(session) != "have prediction!":
        time.sleep(5)
        callback(message, user_id, data)
    else:
        response = data.load_output_data(session)
        transaction = Transaction()
        transaction.write_off(session=session, user_id=user_id, value=100)
        bot.send_message(chat_id, response)
        user_menu(message, user_id)


#  Ниже закоментированы методы, работающие без RabbitMQ
# def pred(message, user_id):
#     chat_id = message.chat.id
#     data = message.text
#     model = OperModel()
#     response = model.response(data)
#     # predict = "Зачем тебе это знать? \nТы и так умница. \nС тебя сотка."
#     transaction = Transaction()
#     transaction.write_off(user_id=user_id, value=100)
#     bot.send_message(chat_id, response)
#     save_data(message, user_id, data, response)


# def save_data(message, user_id, input_data, output_data):
#     data = OperData(input_data, user_id)
#     data.save_input_data()
#     data.save_output_data(output_data)
#     user_menu(message, user_id)


# проверка баланса
@bot.callback_query_handler(func=lambda call: call.data.startswith("balance"))
def check_bal(call):
    message = call.message
    chat_id = message.chat.id
    data_parts = call.data.split("/")
    if len(data_parts) == 2 and data_parts[0] == "balance":
        user_id = data_parts[1]
        user = User(user_id=user_id)
        balance = user.check_balance(session=session)
        bot.send_message(chat_id, f"Твой баланс: {balance}")
        user_menu(message, user_id)
    else:
        bot.send_message(chat_id, "Извини, но я прилег.\nПопробуй позже.")


print("Ready to work! To exit, press Ctrl+C")
bot.infinity_polling()
