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
    closest_places = process_places(user_location)
    for place, distance in closest_places:
        send_place_info(message, place)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_geo = KeyboardButton(text="Send geo-location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Press the button to send your geo-location", reply_markup=keyboard)


def process_places(user_location):
    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    distances = []
    for place in places:
        distances.append((place, geodesic(user_location, (place[3], place[4])).km))
    distances.sort(key=lambda x: x[1])
    return distances[:2]


def send_place_info(message, place):
    photo = open(f"{place[6]}", 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, f"{place[0]}\n{place[1]}\n{place[5]}")
    bot.send_message(message.chat.id, f"Google map:\n{place[2]}")
    bot.send_venue(message.chat.id, place[3], place[4], f"{place[0]}", f"{place[1]}")



connection = psycopg2.connect(
    host="localhost",
    database="telegram_db",
    user="tg_bot",
    password="qwerty"
)
cursor = connection.cursor()


bot.polling()
