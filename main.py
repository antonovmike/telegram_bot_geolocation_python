import psycopg2
import telebot
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    bot.reply_to(message, "Hi, send me your location")


connection = psycopg2.connect(
    host="localhost",
    database="telegram_db",
    user="tg_bot",
    password="qwerty"
)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS places (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        google_map VARCHAR(255)
    )
""")
connection.commit()

bot.polling()
