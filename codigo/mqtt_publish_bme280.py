#!/usr/bin/python3

v ='0.2'

import time

import paho.mqtt.client as mqtt # Import the MQTT library

import utils
import myBme280
import MQTTUtils
import config

myBme280.init()

client = MQTTUtils.initMQTT(clientID = 'b280SensorPublisher',topic2Subscribe='',mqttServer = config.MQTT_SERVER,mqttPort = config.MQTT_PORT)

while True:
    temperature, pressure, humidity, timestamp, id = myBme280.getData()
    MQTTUtils.publish(client,config.BaseTopic_sub + '/Temperatura', f'{temperature:2.2f}'.encode('utf8'))
    MQTTUtils.publish(client,config.BaseTopic_sub + '/Presion', f'{pressure:2.2f}'.encode('utf8'))
    MQTTUtils.publish(client,config.BaseTopic_sub + '/Humedad', f'{humidity:2.2f}'.encode('utf8'))
    data = {}
    data["meteoSalon"] = {"Temperatura": temperature,"Presion":pressure,"Humedad":humidity}
    MQTTUtils.publish(client,config.BaseTopic_sub + '/meteoData', str(data).replace("'",'"').encode('utf8'))
    time.sleep(60)
