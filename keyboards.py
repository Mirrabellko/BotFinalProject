
from telebot.types import *

def start_markup():

    markup = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton(text='Регистрация', callback_data='register')
    button2 = InlineKeyboardButton(text='Вход', callback_data='login')
    
    markup.add(button1, button2)
    
    return markup

