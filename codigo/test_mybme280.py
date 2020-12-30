#!/usr/bin/python3

import time

import utils
import myBme280

myBme280.init()

while True:
    myBme280.getData()
    time.sleep(1)
