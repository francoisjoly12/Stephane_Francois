import board
import busio
import digitalio
import time
import adafruit_bmp280
import projet2
import json
import adafruit_sdcard
import busio
import storage
import pcf8523
from collections import OrderedDict
import adafruit_ntp
import rtc
import adafruit_dht
from adafruit_motor.motor import DCMotor
from pwmio import PWMOut

pvm1 = PWMOut(board.IO13)
pvm2 = PWMOut(board.IO14)

motor = DCMotor(pvm1, pvm2)

throttle = 1.0

time1 = time.monotonic()

while True:
    if(time.monotonic() - time1 > 1):
        time1 = time.monotonic()
        if throttle < 0.0:
            throttle =0.5
        else:
            throttle =-0.5

    motor.throttle = throttle
