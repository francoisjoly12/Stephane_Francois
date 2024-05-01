import board
import digitalio
import time
import busio
import adafruit_dht
from adafruit_motor.motor import DCMotor
from pwmio import PWMOut


dht = adafruit_dht.DHT11(board.IO8)
pvm1 = PWMOut(board.IO13)
pvm2 = PWMOut(board.IO14)
motor = DCMotor(pvm1, pvm2)
throttle = 0
time1 = time.monotonic()

while True:
    if(time.monotonic() - time1 > 1):
        time1 = time.monotonic()
        if dht.humidity < 20:
            throttle = 0
        elif dht.humidity < 25:
            throttle = 0.3
        elif dht.humidity < 30:
            throttle = 0.4
        elif dht.humidity < 35:
            throttle = 0.5
        elif dht.humidity < 40:
            throttle = 0.6
        elif dht.humidity < 45:
            throttle = 0.7
        elif dht.humidity < 50:
            throttle = 0.8
    
        #print(throttle)
        #print(dht.humidity)

    motor.throttle = throttle

    # dans D8 + VCC jaune dans A0