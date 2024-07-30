import telebot

from collections import namedtuple

from config import TOKEN
import database as db
import keyboards as kb
from dbhandlers import *

bot = telebot.TeleBot(TOKEN)

Recipe = namedtuple('Recipe', ['title', 'category', 'ingredients', 'steps', 'cook_time'])
User = namedtuple('User', ['username', 'password', 'email', 'telegram_id'], defaults=(None, None, None))

USER_AUTHORIZATED = False

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


@bot.message_handler(func=lambda message: message.text == 'Главное меню')
def menu_callback_good(message):
    '''
    Обработчик колбека Главное меню
    '''

    print("INFO:: enter to register_callback")

    markup = kb.create_markup(kb.menu_recipe)
      
    bot.send_message(message.chat.id, 'Выбирай!', reply_markup= markup)


@bot.callback_query_handler(func=lambda call: call.data == 'register')
def register_callback(callback):
    '''
    Обработчик колбека register
    '''

    print("INFO:: enter to register_callback")
        
    markup = kb.create_reply(kb.menu_reply)

    bot.send_message(callback.message.chat.id, 'Главное меню', reply_markup= markup)


@bot.callback_query_handler(func=lambda call: call.data == 'login')
def login_callback(callback):
    '''
    Обработчик колбека login
    '''

    print("INFO:: enter to login_callback")
        
    bot.send_message(callback.message.chat.id, 'Введите по образцу:\nlog логин пароль')


@bot.message_handler(func=lambda m: m.text.startswith('log'))
def log_handler(message):
    '''
    Обработчик регистрации и входа в систему
    '''

    print("INFO:: enter to log handler")

    global new_user

    command = message.text.replace('log ', '').split()

    if len(command) == 3:
        new_user = User(command[0], command[1], command[2], message.from_user.id)
    
    else:
        new_user = User(command[0], command[1])

    print(f"login:{new_user.username}, password: {new_user.password}, email: {new_user.email}")


    user_handler = UserHandler(new_user)

    markup = kb.create_markup(kb.menu_recipe)

    if not user_handler.search():

        if user_handler.add_new():
            bot.send_message(message.chat.id, 'Вход выполнен', reply_markup=markup)
            USER_AUTHORIZATED = True
            return

        else:
            bot.send_message(message.chat.id, 'Попробуй еще раз ввести данные по образцу:\nlog логин пароль')

    if user_handler.check_password():
        bot.send_message(message.chat.id, 'Вход выполнен', reply_markup=markup)
        USER_AUTHORIZATED = True

    else:
        bot.send_message(message.chat.id, 'Ошибка в пароле!')

    #bot.register_next_step_handler(message, add_recipe, new_user.username)

@bot.callback_query_handler(func=lambda call: call.data == 'add_recipe')
def add_recipe_callback(callback):
    '''
    Обработчик добавления нового рецепта
    '''
    print("INFO:: enter to add_recipe_callback")

    text = 'Введите по образцу:\nadd::\nНазвание рецепта::\nВид блюда::\nИнгридиенты::\nШаги приготовления::\nВремя приготовления'
        
    bot.send_message(callback.message.chat.id, text)


@bot.message_handler(func=lambda m: m.text.startswith('add'))
def add_recipe(message):
    '''
    Обработчик добавления нового рецепта
    '''
    print("INFO:: enter to add_recipe")

    command = message.text.split('::')

    user_recipe = Recipe(command[1], command[2], command[3], command[4], command[5])

    print(f'Рецепт\nНазвание: {user_recipe.title}\nВид блюда: {user_recipe.category}\nИнгридиенты: {user_recipe.ingredients}\nШаги приготовления: {user_recipe.steps}\nВремя приготовления: {user_recipe.cook_time}')

    username = new_user.username

    recipe_handler = RecipeHandler(username, user_recipe)

    markup = kb.create_reply(kb.menu_reply)

    if recipe_handler.add_new():
        bot.send_message(message.chat.id, 'Рецепт добавлен', reply_markup= markup)
    
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так...Попробуй еще раз!', reply_markup= markup)

    

@bot.callback_query_handler(func=lambda call: call.data == 'view_recipes')
def view_recipies_callback(callback):
    '''
    Просмотр всех рецептов пользователя
    '''
    username = new_user.username
    
    recipe_handler = RecipeHandler(username)

    result = recipe_handler.search()

    markup = kb.create_reply(kb.menu_reply)

    bot.send_message(callback.message.chat.id, result, reply_markup= markup)


@bot.callback_query_handler(func=lambda call: call.data == 'view_one')
def view_one_recipe_callback(callback):
    '''
    Просмотр одного рецепта пользователя
    '''
    bot.send_message(callback.message.chat.id, 'Введите название рецепта по образцу:\nfind Название рецепта')


@bot.message_handler(func=lambda m: m.text.startswith('find'))
def view_one_recipe_final(message):
    '''
    Просмотр одного рецепта пользователя
    '''
    title = message.text.replace('find ', '')

    username = new_user.username

    recipe_handler = RecipeHandler(username)

    result = recipe_handler.search(title)

    markup = kb.create_reply(kb.menu_reply)

    bot.send_message(message.chat.id, result, reply_markup= markup)


@bot.callback_query_handler(func=lambda call: call.data == 'delete')
def delete_recipe_callback(callback):
    '''
    Удаление рецепта
    '''
    bot.send_message(callback.message.chat.id, 'Введите команду для удаления рецепта по образцу:\ndel Название рецепта')


@bot.message_handler(func=lambda m: m.text.startswith('del'))
def delete_recipe_final(message):
    '''
    Удаление одного рецепта пользователя
    '''
    title = message.text.replace('del ', '')

    username = new_user.username

    recipe_handler = RecipeHandler(username)

    if recipe_handler.delete(title):
        markup = kb.create_reply(kb.menu_reply)
        bot.send_message(message.chat.id, 'Рецепт был удален', reply_markup= markup)

    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так...')






if __name__ == "__main__":
    bot.infinity_polling()