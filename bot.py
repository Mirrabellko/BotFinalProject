import telebot

from collections import namedtuple

from config import TOKEN
import database as db
import keyboards as kb

bot = telebot.TeleBot(TOKEN)

Recipe = namedtuple('Recipe', ['title', 'category', 'ingredients', 'steps', 'cook_time'])
User = namedtuple('User', ['username', 'password', 'email'])

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


@bot.message_handler(func=lambda m: m.text.startswith('log')) # -log login password
def register(message):

    print("INFO:: register")
    command = message.text.replace('log ', '')

# Продолжить отсюда
    login, password = tuple(command.split(' '))
    print(f"login:{login}, password: {password}")

    if db_registration(login, password):
        markup = kb.question()
        user_state = ClientState(QuestionState)
        bot.send_message(message.chat.id, 'Вход выполнен', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Попробуй еще раз ввести данные по образцу:\nlog логин пароль')
        
        




if __name__ == "__main__":
    bot.infinity_polling()