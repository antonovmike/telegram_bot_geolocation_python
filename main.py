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
    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    distances = []
    for place in places:
        print(place[3], place[4])
        print(geodesic(user_location, (place[3], place[4])).km, place)
        distances.append((place, geodesic(user_location, (place[3], place[4])).km))
    print(f"Distances not sorted: {distances}")
    distances.sort(key=lambda x: x[1])
    print(f"Distances sorted:     {distances}")
    for place, distance in distances[:2]:
        print(f"Distance: {distance}")
        photo = open(f"{place[6]}", 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, f"{place[0]}\n{place[1]}\n{place[5]}")
        bot.send_message(message.chat.id, f"Google map:\n{place[2]}")
        bot.send_venue(message.chat.id, place[3], place[4], f"{place[0]}", f"{place[1]}")


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


bot.polling()
