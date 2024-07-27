
from telebot.types import *

def create_markup(buttons: dict):

    markup = InlineKeyboardMarkup()

    for key, value in buttons:

        new_button = InlineKeyboardButton(text=buttons[value], callback_data=buttons[key])
    
        markup.add(new_button)
    
    return markup

