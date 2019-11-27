#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""

import logging
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
import requests
import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import datetime

MQTT_SERVER = "192.168.1.200"

update_id = None

user_keyboard = [['/red','/blue'],['/green', '/black'],['/help','/free']]
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)

# Our "on message" event
def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    myLog(topic + ' - ' + message)

def myLog(message):
    print(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f "))+ message)
    
def initMQTT():
    global ourClient
    ourClient = mqtt.Client("CBT_bot_mqtt") # Create a MQTT client object with this id
    ourClient.connect(MQTT_SERVER, 1883) # Connect to the test MQTT broker
    myLog('Conectado a MQTT broker '+MQTT_SERVER)
    ourClient.subscribe("MeteoSalon/#") # Subscribe to the topic AC_unit
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
    ourClient.loop_start() # Start the MQTT client
    myLog('MQTT client started')

def main():
    """Run the bot."""
    global update_id
    
    initMQTT()
    
    # Telegram Bot Authorization Token
    bot = telegram.Bot('12341234:PON-AQUI-TU-TOKEN')


    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    last_pub = int(round(time.time() * 1000))
    while True:
        try:
            now = int(round(time.time() * 1000))
            if (now - last_pub) > 5000: # 5 segundos
                ourClient.publish("MeteoSalon/BotMQTTTest", "MQTT Bot") # Publish message to MQTT broker
                last_pub = now
            updateBot(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        except :
            myLog('Excepcion!!')


# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES TELERAM
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm


def get_url(url):
    '''
    Funcion de apoyo a la recogida de telegramas,
    Recoge el contenido desde la url de telegram
    '''
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def send_message(text, chat_id):
    '''
    Funcion para enviar telergamas atraves de la API
    '''
    try:
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        #print("url >> ",url)
        get_url(url)
    except:
        print("ERROR de envio")

def updateBot(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            comando = update.message.text  #MENSAJE_RECIBIDO
            chat_time = update.message.date
            user = update.message.from_user #USER_FULL
            chat_id = int(update.message.from_user.id)
            user_real_name = user.first_name #USER_REAL_NAME
            print('Comand: '+comando)
            if comando == '/start':
                update.message.reply_text("Bienvenido al Bot casero v0.0", reply_markup=user_keyboard_markup)
            elif comando == 'hi':
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
            elif comando == '/red':
                ourClient.publish("MeteoSalon/ledRGB", "Red") # Publish message to MQTT broker
            elif comando == '/blue':
                ourClient.publish("MeteoSalon/ledRGB", "Blue") # Publish message to MQTT broker
            elif comando == '/green':
                ourClient.publish("MeteoSalon/ledRGB", "Green") # Publish message to MQTT broker
            elif comando == '/black':
                ourClient.publish("MeteoSalon/ledRGB", "Black") # Publish message to MQTT broker
            elif comando == '/help':
                send_message (listaComandosTxt, chat_id)
            elif comando == '/free':
                ourClient.publish("MeteoSalon/free", "Free") # Publish message to MQTT broker
            else:
                update.message.reply_text('echobot: '+update.message.text)


if __name__ == '__main__':
    main()