
from telebot.types import *

menu_reply = {'start': 'Главное меню'}

menu_recipe = {
        'add_recipe': 'Добавить новый рецепт',
        'view_recipes': 'Просмотреть все рецепты',
        'view_one': 'Поиск рецепта по названию',
        'delete': 'Удалить рецепт'
        }


def create_markup(buttons: dict):

    markup = InlineKeyboardMarkup()

    keys = buttons.keys()

    for key in keys:

        new_button = InlineKeyboardButton(text=buttons[key], callback_data=key)
    
        markup.add(new_button)
    
    return markup


def create_reply(buttons: dict):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keys = buttons.keys()

    for key in keys:

        new_button = KeyboardButton(text=buttons[key])
    
        markup.add(new_button)
    
    return markup