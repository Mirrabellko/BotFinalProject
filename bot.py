import telebot

from collections import namedtuple

from config import TOKEN
import database as db
import keyboards as kb
from dbhandlers import *

bot = telebot.TeleBot(TOKEN)

Recipe = namedtuple('Recipe', ['title', 'category', 'ingredients', 'steps', 'cook_time'])
User = namedtuple('User', ['username', 'password', 'email'], defaults=(None, None, None))

def user_data():

    status = None
    user = None

    def closure(new_user: namedtuple):

        user = new_user
        print(f"user: {user}")

        return user

    return closure

def recipe_data():

    user_recipe = None

    def closure(recipe: namedtuple):

        user_recipe = recipe
        print(f"recipe: {user_recipe}")

        return user_recipe

    return closure




# Обработчики

@bot.message_handler(commands=['start'])
def start_handler( message):
    '''
    Обработчик команды start
    '''

    print("INFO:: enter to start_handler")
    text = 'Добро пожаловать в Книгу Рецептов'

    markup = kb.create_markup({
        'register': 'Начать использование!',
        'login': 'Вход в систему'
        })

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'register')
def register_callback(callback):
    '''
    Обработчик колбека register
    '''

    print("INFO:: enter to register_callback")
        
    bot.send_message(callback.message.chat.id, 'Введите по образцу:\nlog логин пароль email')


@bot.callback_query_handler(func=lambda call: call.data == 'login')
def login_callback(callback):
    '''
    Обработчик колбека login
    '''

    print("INFO:: enter to login_callback")
        
    bot.send_message(callback.message.chat.id, 'Введите по образцу:\nlog логин пароль')


@bot.message_handler(func=lambda m: m.text.startswith('log'))
def log_handler(message):

    print("INFO:: enter to log handler")

    command = message.text.replace('log ', '').split()

    if len(command) == 3:
        new_user = User(command[0], command[1], command[2])
    
    else:
        new_user = User(command[0], command[1])

    print(f"login:{new_user.username}, password: {new_user.password}, email: {new_user.email}")

    user_handler = UserHandler(new_user)

    markup = kb.create_markup({
        'add_recipe': 'Добавить новый рецепт',
        'view_recipes': 'Просмотреть все рецепты',
        'view_one': 'Поиск рецепта по названию',
        'delete': 'Удалить рецепт'
        })

    if not user_handler.search():
        if user_handler.add_new():
            bot.send_message(message.chat.id, 'Вход выполнен', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Попробуй еще раз ввести данные по образцу:\nlog логин пароль')





if __name__ == "__main__":
    bot.infinity_polling()