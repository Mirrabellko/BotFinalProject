import telebot

from collections import namedtuple

from config import TOKEN
import database as db

bot = telebot.TeleBot(TOKEN)

Recipe = namedtuple('Recipe', ['title', 'category', 'ingredients', 'steps', 'cook_time'])
User = namedtuple('User', ['username', 'password', 'email'])

def user_data():

    status = None
    user = None

    def closure(new_user: namedtuple):

        user = new_user
        print(f"user: {user}")

        return closure

def recipe_data():

    user_recipe = None

    def closure(recipe: namedtuple):

        user_recipe = recipe
        print(f"recipe: {user_recipe}")

        return closure



        
        




if __name__ == "__main__":
    bot.infinity_polling()