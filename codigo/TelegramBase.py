# Telegram

# TELEGRAM
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized



# ACCESO A DATOS EN SERVIDORES (usado por telegram)
#import json 
import requests


import config
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES TELEGRAM
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm



#URL de la API de TELEGRAM
URL = "https://api.telegram.org/bot{}/".format(config.TELEGRAM_API_TOKEN)

def get_url(url):
    '''
    Funcion de apoyo a la recogida de telegramas,
    Recoge el contenido desde la url de telegram
    '''
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def send_picture(picture):
    url = URL+"sendPhoto";
    files = {'photo': open(picture, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

def send_document(doc):
    url = URL+"sendDocument";
    files = {'document': open(doc, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def send_message(text):
    '''
    Funcion para enviar telegramas atraves de la API
    '''
    try:
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        #print("url >> ",url)
        get_url(url)
    except:
        print("ERROR de envio")

