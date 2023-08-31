import telebot
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    bot.reply_to(message, "Hi, send me your location")


bot.polling()
