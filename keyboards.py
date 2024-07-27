
from telebot.types import *

def create_markup(buttons: dict):

    markup = InlineKeyboardMarkup()

    keys = buttons.keys()

    for key in keys:

        new_button = InlineKeyboardButton(text=buttons[key], callback_data=key)
    
        markup.add(new_button)
    
    return markup

