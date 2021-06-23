import config
import telebot
import requests
from bs4 import BeautifulSoup as BS
from telebot import types
import emoji            # emoji lib

# Парсинг сайта 
r = requests.get("https://sinoptik.ua/погода-калининград")
html = BS(r.content, 'html.parser')
bot = telebot.TeleBot(config.token)

# Парсинг информации с сайта 
for el in html.select('#content'):
    data = el.select('.date ')[0].text
    day = el.select('.day-link ')[0].text
    month= el.select('.month ')[0].text
    temp_min = el.select('.temperature .min ')[0].text
    temp_max = el.select('.temperature .max ')[0].text
    text =el.select('.wDescription .description')[0].text
    feels_like =el.select('.temperatureSens .p5')[0].text
    img = el.select('.weatherIcoS .weatherIco ')[0].img
    sunrise =el.select('.infoDaylight ')[0].text

#Вывод кнопок при старте бота  
@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Узнать погоду на сегодня')
    markup.add(itembtn1)
    msg = bot.send_message(message.chat.id,
                    "Привет" +(emoji.emojize(':raised_hand:')) +  message.from_user.first_name  + "\n Я бот пока только умею показывать"+(emoji.emojize(':cloud:'))+"погоду в городе Калининграде"+(emoji.emojize(':house_with_garden:')) +" ", reply_markup=markup)
    
    bot.register_next_step_handler(msg,SendWeather)



#Вывод данных
@bot.message_handler(func=lambda message: True , content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def SendWeather(message):
    bot.reply_to(message,emoji.emojize(':calendar:Сегодня {0} {1} {2} \n' '\n'
    ':sun_with_face: Температура в течении дня {3} {4} \n' '\n' ':cloud: Ошущается как {5} \n''\n'':sunrise_over_mountains: {6} \n''\n'':cloud:{7}').format(day,data,month, temp_min,temp_max,feels_like ,sunrise ,text ))

bot.polling()  
