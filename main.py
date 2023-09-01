# import pandas as pd
import psycopg2
import os
import telebot
from dotenv import load_dotenv
from geopy.distance import geodesic
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_location = (message.location.latitude, message.location.longitude)
    print(f"User location: {user_location}")
    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    print(f"Places: {places}")
    distances = [(place, geodesic(user_location, (place[3], place[4])).km) for place in places]
    print(f"Distances: {distances}")
    distances.sort(key=lambda x: x[1])
    for place, distance in distances[:2]:
        photo = open(f"{place[6]}", 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, f"{place[0]}\n{place[1]}\n{place[2]}\n{place[5]}")


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_geo = KeyboardButton(text="Send geo-location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Press the button to send your geo-location", reply_markup=keyboard)


connection = psycopg2.connect(
    host="localhost",
    database="telegram_db",
    user="tg_bot",
    password="qwerty"
)
cursor = connection.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS places (
#         name VARCHAR(255),
#         address VARCHAR(255),
#         google_map VARCHAR(255),
#         latitude INT,
#         longitude INT,
#         description TEXT,
#         picture VARCHAR(255)
#     )
# """)
# connection.commit()
#
#
# def update_places():
#     df = pd.read_excel('catalog.ods')
#     for index, row in df.iterrows():
#         cursor.execute(
#             """
#             INSERT INTO places (name, address, google_map, latitude, longitude, description, picture)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#             """,
#             (row['name'], row['address'], row['google_map'], row['latitude'], row['longitude'], row['description'],
#              row['picture'])
#         )
#     connection.commit()


bot.polling()
