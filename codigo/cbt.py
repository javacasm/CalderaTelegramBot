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

import sys
import config
import utils
import TelegramBase
import MQTTUtils
import Caldera

v = '1.2'

update_id = None

# 'keypad' buttons
user_keyboard = [['/help','/info'],['/calderaOn', '/calderaOff']]
# user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard)

commandList = '/help, /info, /calderaOn, /calderaOff'

bEsperandoRespuestaCaldera = False
last_CalderaStatusCheck = int(round(time.time() * 1000))

def main():
    """Run the bot."""
    global update_id
    global chat_id
    global ourClient
    global bEsperandoRespuestaCaldera, last_CalderaStatusCheck
    ourClient = MQTTUtils.initMQTT()
    
    bot = telegram.Bot(config.TELEGRAM_API_TOKEN)
    
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
        
    utils.myLog('Init TelegramBot')
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    last_Beat = int(round(time.time() * 1000))
    while True:
        try:
            now = int(round(time.time() * 1000))
            if (now - last_Beat) > 60000: # 60 segundos
                MQTTUtils.publish(ourClient,config.BaseTopic_sub + "/BotMQTTTest", "MQTT Bot") # Publish message to MQTT broker
                utils.myLog('Sent BotMQTTTest')
                last_Beat = now
            if bEsperandoRespuestaCaldera : # and (now - last_CalderaStatusCheck ) > 1000:  # 1 segundo    
                if Caldera.MQTT_caldera_Status in MQTTUtils.MQTTData:
                    print('Tiempo desde comando ',now - last_CalderaStatusCheck)
                    date, value = MQTTUtils.getData(Caldera.MQTT_caldera_Status)
                    TelegramBase.send_message('Caldera '+ value + ' @ ' + date ,chat_id)
                    bEsperandoRespuestaCaldera = False
                elif (now - last_CalderaStatusCheck ) > 10000 : 
                    TelegramBase.send_message('Sin respuesta de la caldera tras ' + str((now - last_CalderaStatusCheck )//1000)+ ' segundos',chat_id)
            updateBot(bot)
            if MQTTUtils.bUpdateCalderaStatus:
                MQTTUtils.bUpdateCalderaStatus = False
                if MQTTUtils.getData(config.topicCalderaStatus) == 'On':
                    MQTTUtils.publish(ourClient,config.topicLedRGB,"Red")
                else
                    MQTTUtils.publish(ourClient,config.topicLedRGB,"Blue")
                time.sleep_ms(100)
                MQTTUtils.publish(ourClient,config.topicLedRGB,"Black")
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        except KeyboardInterrupt:
            utils.myLog('Interrupted')
            sys.exit(0)            
        except Exception as e:
            utils.myLog('Excepcion!!: ' + str(e))

botCommandsMQTT ={'/black':[config.BaseTopic_sub+"/ledRGB", "Black"], '/red':[config.BaseTopic_sub+"/ledRGB", "Red"],
'/blue':[config.BaseTopic_sub+"/ledRGB", "Blue"], '/green':[config.BaseTopic_sub+"/ledRGB", "Green"],'/free':[config.BaseTopic_sub+"/Free", "Free"]}

# Update and chat with the bot
def updateBot(bot):
    """Answer the message the user sent."""
    global update_id
    global ourClient
    global bEsperandoRespuestaCaldera, last_CalderaStatusCheck
    global chat_id
    #utils.myLog('Updating telegramBot')
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
            utils.myLog('Command: '+comando+' from user ' + str(user_real_name )+' in chat id:' + str(update.message.from_user.id)+ ' at '+str(command_time))
            if comando == '/start':
                update.message.reply_text("Bienvenido al Bot casero v0.1", reply_markup=user_keyboard_markup)
            elif comando == 'hi':
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name), reply_markup=user_keyboard_markup)
            elif comando == '/info':
                answer = 'Datos @ ' + utils.getStrDateTime() + '\n==========================\n\n' + MQTTUtils.getFullData()
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == '/info+':
                answer = 'Datos @ ' + utils.getStrDateTime() + '\n==========================\n\n' + MQTTUtils.getFullDataDate()
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == '/help':
                bot.send_message(chat_id = chat_id, text = commandList, reply_markup = user_keyboard_markup)
            elif comando == '/calderaOn':
                MQTTUtils.deleteTopic(Caldera.MQTT_caldera_Status) # Para mostrar el nuevo valor
                #resultado = Caldera.calderaWebOn()
                resultado = Caldera.calderaMQTTOn(ourClient)
                last_CalderaStatusCheck = int(round(time.time() * 1000))                
                update.message.reply_text('Enviada orden de encendido a la Caldera', reply_markup=user_keyboard_markup)
                bEsperandoRespuestaCaldera = True
            elif comando == '/calderaOff':
                MQTTUtils.deleteTopic(Caldera.MQTT_caldera_Status) # Para mostrar el nuevo valor
                #resultado = Caldera.calderaWebOff()
                resultado = Caldera.calderaMQTTOff(ourClient)
                last_CalderaStatusCheck = int(round(time.time() * 1000))
                update.message.reply_text('Enviada orden de apagado a la Caldera', reply_markup=user_keyboard_markup)
                bEsperandoRespuestaCaldera = True
            elif comando in botCommandsMQTT:
                MQTTUtils.publish(ourClient, botCommandsMQTT[comando][0], botCommandsMQTT[comando][1]) # Publish message to MQTT broker
                TelegramBase.send_message ('Sent '+comando+'MQTT command',chat_id)
            else:
                update.message.reply_text('echobot: '+update.message.text, reply_markup=user_keyboard_markup)                

if __name__ == '__main__':
    main()
