import board
import digitalio
import time
import busio
import adafruit_dht
from adafruit_motor.motor import DCMotor
from pwmio import PWMOut

class motor:
    def __init__(self, dht_pin, motor_pvm1, motor_pvm2):
        self.dht = adafruit_dht.DHT11(board.IO8)
        self.motor = DCMotor(PWMOut( board.IO13), PWMOut(board.IO14))
        self.throttle = 0
        self.time1 = time.monotonic()

    def run(self):
        while True:
            if(time.monotonic() - self.time1 > 1):
                self.time1 = time.monotonic()
                if self.dht.humidity < 20:
                    self.throttle = 0
                elif self.dht.humidity < 25:
                    self.throttle = 0.3
                elif self.dht.humidity < 30:
                    self.throttle = 0.4
                elif self.dht.humidity < 35:
                    self.throttle = 0.5
                elif self.dht.humidity < 40:
                    self.throttle = 0.6
                elif self.dht.humidity < 45:
                    self.throttle = 0.7
                elif self.dht.humidity < 50:
                    self.throttle = 0.8
                #print("Humidity:", self.dht.humidity)
                #print("Throttle:", self.throttle)
            
            self.motor.throttle = self.throttle
