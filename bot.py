import telebot

from config import TOKEN


bot = telebot.TeleBot(TOKEN)


if __name__ == "__main__":
    bot.infinity_polling()