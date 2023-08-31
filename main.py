import pandas as pd
import psycopg2
import os
import telebot
from dotenv import load_dotenv
from geopy.distance import geodesic

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
            VALUES (%s, %s, %s, %s)
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
