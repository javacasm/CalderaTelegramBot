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
    global bEsperandoRespuestaCaldera
    global last_CalderaStatusCheck 
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
            if bEsperandoRespuestaCaldera and (now - last_CalderaStatusCheck ) > 3000:  # 3 segundos    
                if Caldera.MQTT_caldera_Status in MQTTUtils.MQTTData:
                    TelegramBase.send_message('Caldera '+ MQTTUtils.MQTTData[Caldera.MQTT_caldera_Status][1],chat_id)
                    bEsperandoRespuestaCaldera = False
                else: 
                    TelegramBase.send_message('Sin respuesta de la caldera ',chat_id)
            updateBot(bot)
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
    global bEsperandoRespuestaCaldera
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
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
            elif comando == '/info':
                answer = 'Datos @ ' + utils.getStrDateTime() + '\n==========================\n\n'
                for item in MQTTUtils.MQTTData:
                    if item.startswith(config.BaseTopic_sub):
                        answer += '**'+item[len(config.BaseTopic_sub)+1:]+ '** ' + MQTTUtils.MQTTData[item][1] + '\n'
                    else:
                        answer += item + ' ' + MQTTUtils.MQTTData[item][1] + '\n'
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN)             
            elif comando == '/info+':
                answer = utils.getStrDateTime() + '\n'
                for item in MQTTUtils.MQTTData:
                    answer += item + '@' + MQTTUtils.MQTTData[item][0] + ' ' + MQTTUtils.MQTTData[item][1] + '\n'
                update.message.reply_text(answer)
            elif comando == '/help':
                TelegramBase.send_message (commandList, chat_id)
            elif comando == '/calderaOn':
                #resultado = Caldera.calderaWebOn()
                resultado = Caldera.calderaMQTTOn(ourClient)
                # TelegramBase.send_message ('Caldera '+resultado,chat_id)
                # MQTTUtils.publish(ourClient,config.BaseTopic_sub + '/Caldera',resultado)
                # TelegramBase.send_message ('Enviado encendido de Caldera',chat_id)
                bot.send_message(chat_id=chat_id, text='Enviado encendido de Caldera', reply_markup=user_keyboard_markup)                
                bEsperandoRespuestaCaldera = True
                last_CalderaStatusCheck = int(round(time.time() * 1000))
            elif comando == '/calderaOff':
                #resultado = Caldera.calderaWebOff()
                resultado = Caldera.calderaMQTTOff(ourClient)                
                # TelegramBase.send_message ('Caldera '+resultado,chat_id)
                # MQTTUtils.publish(ourClient,config.BaseTopic_sub + '/Caldera',resultado)
                # TelegramBase.send_message ('Enviado apagado de Caldera',chat_id)
                bot.send_message(chat_id=chat_id, text='Enviado apagado de Caldera', reply_markup=user_keyboard_markup)
                bEsperandoRespuestaCaldera = True
                last_CalderaStatusCheck = int(round(time.time() * 1000))
            elif comando in botCommandsMQTT:
                MQTTUtils.publish(ourClient, botCommandsMQTT[comando][0], botCommandsMQTT[comando][1]) # Publish message to MQTT broker
                TelegramBase.send_message ('Sent '+comando+'MQTT command',chat_id)
            else:
                update.message.reply_text('echobot: '+update.message.text)                

if __name__ == '__main__':
    main()
