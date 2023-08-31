import pandas as pd
import psycopg2
import os
import telebot
from dotenv import load_dotenv
from geopy.distance import geodesic
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    bot.reply_to(message, "Hi, send me your location")


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_geo = KeyboardButton(text="Send geo-location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Press the button to send your geo-location", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    bot.send_message(message.chat.id, f"Your geo-location: {message.location.latitude}, {message.location.longitude}")


connection = psycopg2.connect(
    host="localhost",
    database="telegram_db",
    user="tg_bot",
    password="qwerty"
)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS places (
        name VARCHAR(255),
        address VARCHAR(255),
        google_map VARCHAR(255)
    )
""")
connection.commit()


def update_places():
    df = pd.read_excel('places.ods')
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO places (name, address, google_map)
            VALUES (%s, %s, %s)
            """,
            (row['name'], row['address'], row['google_map'])
        )
    connection.commit()


@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_location = (message.location.latitude, message.location.longitude)
    cursor.execute("SELECT name, address, google_map FROM places")
    places = cursor.fetchall()
    distances = [(place, geodesic(user_location, place['google_map']).miles) for place in places]
    distances.sort(key=lambda x: x[1])
    for place, distance in distances[:2]:
        bot.send_message(message.chat.id,
                         f"Name: {place['name']}\nAddress: {place['address']}\nMap: {place['google_map']}")


bot.polling()
