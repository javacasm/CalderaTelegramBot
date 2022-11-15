#!/usr/bin/python3
"""
Ejemplo de lectura de temperatura, presión y humedad con el sensor bme280
Se requiere el módulo RPi.bme280

Instalación:
pip3 install smbus2
pip3 install RPi.bme280
"""

import smbus2
import bme280

import utils

v = '0.7'

port = 1
address = 0x76 # usaremos la dirección que hemos encontrado

bus = None
calibration_params = None


def init():
    global bus
    global calibration_params
    global bInit

    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address) # parámetros de compensación

def getStrData():
    temperature, pressure, humidity, timestamp, id = getData()
    return 'Temp:{}º Pres:{} mb Hum:{}% at {} id: {}'.format(int(temperature), int(pressure), int(humidity), timestamp, id)


def getData():
    global bus
    global calibration_params

    if calibration_params == None:
        init()
# leemos los datos
    data = bme280.sample(bus, address, calibration_params)

# los mostramos en otro formato
    utils.myLog(str(data))
    return round(data.temperature,2), round(data.pressure,2), round(data.humidity,2), data.timestamp, data.id
