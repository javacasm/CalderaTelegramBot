#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages, get MQTT connection

"""

# Telegram staff: from inopya https://github.com/inopya/mini-tierra

import logging
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
import requests
import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import datetime


# Telegram Bot Authorization Token
TELEGRAM_API_TOKEN = '12341234:PON-AQUI-TU-TOKEN'

MQTT_SERVER = "192.168.1.200"

update_id = None

# 'keypad' buttons
user_keyboard = [['/red','/blue'],['/green', '/black'],['/help','/free']]
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
commandList = '/red, /blue, /green, /black, /help, /free'

def myLog(message):
    print(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f "))+ message)

topic_sub = 'MeteoSalon'



# Our "on message" event
def checkMQTTSubscription (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    #if topic.startswith(topic_sub):
    #    pass ## TODO: check topics
    myLog('MQTT:'+topic + ' - ' + message)
    
def initMQTT():
    global ourClient
    ourClient = mqtt.Client("CBT_bot_mqtt") # Create a MQTT client object with this id
    ourClient.connect(MQTT_SERVER, 1883) # Connect to the test MQTT broker
    myLog('Conectado a MQTT broker '+MQTT_SERVER)
    ourClient.subscribe(topic_sub+'/#') # Subscribe to the topic 
    ourClient.on_message = checkMQTTSubscription # Attach the messageFunction to subscription
    ourClient.loop_start() # Start the MQTT client
    myLog('MQTT client started')

def main():
    """Run the bot."""
    global update_id
    
    initMQTT()
    
    bot = telegram.Bot(TELEGRAM_API_TOKEN)
    
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
        
    myLog('Init TelegramBot')
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    last_pub = int(round(time.time() * 1000))
    while True:
        try:
            now = int(round(time.time() * 1000))
            if (now - last_pub) > 5000: # 5 segundos
                ourClient.publish("MeteoSalon/BotMQTTTest", "MQTT Bot") # Publish message to MQTT broker
                myLog('Sent MQTT test')
                last_pub = now
            updateBot(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        except :
            myLog('Excepcion!!')


# Telegram staff: from inopya https://github.com/inopya/mini-tierra
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

#URL de la API de TELEGRAM
URL_API_TELEGRAM = "https://api.telegram.org/bot{}/".format(TELEGRAM_API_TOKEN)

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
        url = URL_API_TELEGRAM + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        #print("url >> ",url)
        get_url(url)
    except:
        print("ERROR de envio")

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm


# Update and chat with the bot
def updateBot(bot):
    """Answer the message the user sent."""
    global update_id
    myLog('Updating telegramBot')
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Proccess the incoming message
            comando = update.message.text  # message text
            command_time = update.message.date # command date
            user = update.message.from_user #User full objetct
            chat_id = int(update.message.from_user.id)
            user_real_name = user.first_name #USER_REAL_NAME
            myLog('Command: '+comando+' from user ' + str(user_real_name )+' in chat id:' + str(update.message.from_user.id)+ ' at '+str(command_time))
            if comando == '/start':
                update.message.reply_text("Bienvenido al Bot casero v0.0", reply_markup=user_keyboard_markup)
            elif comando == 'hi':
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
            elif comando == '/red':
                ourClient.publish("MeteoSalon/ledRGB", "Red") # Publish message to MQTT broker
                send_message ('Sent '+comando+'MQTT command', chat_id)
            elif comando == '/blue':
                ourClient.publish("MeteoSalon/ledRGB", "Blue") # Publish message to MQTT broker
                send_message ('Sent '+comando+'MQTT command', chat_id)
            elif comando == '/green':
                ourClient.publish("MeteoSalon/ledRGB", "Green") # Publish message to MQTT broker
                send_message ('Sent '+comando+'MQTT command', chat_id)
            elif comando == '/black':
                ourClient.publish("MeteoSalon/ledRGB", "Black") # Publish message to MQTT broker
                send_message ('Sent '+comando+'MQTT command', chat_id)
            elif comando == '/help':
                send_message (commandList, chat_id)
            elif comando == '/free':
                ourClient.publish("MeteoSalon/free", "Free") # Publish message to MQTT broker
                send_message ('Sent '+comando+'MQTT command', chat_id)                
            else:
                update.message.reply_text('echobot: '+update.message.text)


if __name__ == '__main__':
    main()