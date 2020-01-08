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
import sys
import config


update_id = None

# 'keypad' buttons
user_keyboard = [['/red','/blue'],['/green', '/black'],['/help','/free'],['/info','/info+']]
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
commandList = '/red, /blue, /green, /black, /help, /free, /info, /info+'

def getStrDateTime():
    return str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) 

def getStrDateTimeMilis():
    return str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")) 

def myLog(message):
    print(getStrDateTime()+ " " + message)

Data = { 'initTime' : [getStrDateTime() , getStrDateTime()] }

# Our "on message" event
def checkMQTTSubscription (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    #if topic.startswith(topic_sub):
    #    pass ## TODO: check topics
    Data[topic] = [ getStrDateTime() , message]
    
    myLog('MQTT: '+getStrDateTime() + ' ' +topic + ' - ' + message)
    
def initMQTT():
    global ourClient
    ourClient = mqtt.Client("CBT_bot_mqtt") # Create a MQTT client object with this id
    ourClient.connect(config.MQTT_SERVER, 1883) # Connect to the test MQTT broker
    myLog('Conectado a MQTT broker ' + config.MQTT_SERVER)
    ourClient.subscribe(config.BaseTopic_sub+'/#') # Subscribe to the topic 
    ourClient.on_message = checkMQTTSubscription # Attach the messageFunction to subscription
    ourClient.loop_start() # Start the MQTT client
    myLog('MQTT client started')

def main():
    """Run the bot."""
    global update_id
    
    initMQTT()
    
    bot = telegram.Bot(config.TELEGRAM_API_TOKEN)
    
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
            if (now - last_pub) > 60000: # 60 segundos
                ourClient.publish(config.BaseTopic_sub + "/BotMQTTTest", "MQTT Bot") # Publish message to MQTT broker
                last_pub = now
            updateBot(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        except KeyboardInterrupt:
            myLog('Interrupted')
            sys.exit(0)            
        except :
            myLog('Excepcion!!')


# Telegram staff: from inopya https://github.com/inopya/mini-tierra
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

#URL de la API de TELEGRAM
URL_API_TELEGRAM = "https://api.telegram.org/bot{}/".format(config.TELEGRAM_API_TOKEN)

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


botCommandsMQTT ={'/black':[config.BaseTopic_sub+"/ledRGB", "Black"], '/red':[config.BaseTopic_sub+"/ledRGB", "Red"],
'/blue':[config.BaseTopic_sub+"/ledRGB", "Blue"], '/green':[config.BaseTopic_sub+"/ledRGB", "Green"],'/free':[config.BaseTopic_sub+"/Free", "Free"]}

# Update and chat with the bot
def updateBot(bot):
    """Answer the message the user sent."""
    global update_id
    #myLog('Updating telegramBot')
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
                update.message.reply_text("Bienvenido al Bot casero v0.1", reply_markup=user_keyboard_markup)
            elif comando == 'hi':
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
            elif comando == '/info':
                answer = 'Datos disponibles @ ' + getStrDateTime() + '\n'
                for item in Data:
                    if item.startswith(config.BaseTopic_sub):
                        answer += item[len(config.BaseTopic_sub)+1] + ' ' + Data[item][1] + '\n'
                    else:
                        answer += item + ' ' + Data[item][1] + '\n'
                update.message.reply_text(answer)             
            elif comando == '/info+':
                answer = getStrDateTime() + '\n'
                for item in Data:
                    answer += item + '@' + Data[item][0] + ' ' + Data[item][1] + '\n'
                update.message.reply_text(answer)                         
            elif comando == '/help':
                send_message (commandList, chat_id)
            elif comando in botCommandsMQTT:
                ourClient.publish(botCommandsMQTT[comando][0], botCommandsMQTT[comando][1]) # Publish message to MQTT broker
                send_message ('Sent '+comando+'MQTT command', chat_id)
            else:
                update.message.reply_text('echobot: '+update.message.text)                

if __name__ == '__main__':
    main()
