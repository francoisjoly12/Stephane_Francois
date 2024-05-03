import board
#motor.py
import time
from adafruit_motor.motor import DCMotor
from pwmio import PWMOut

class motor:
    def __init__(self, motor_pvm1, motor_pvm2):
        self.motor = DCMotor(PWMOut( motor_pvm1), PWMOut(motor_pvm2))
        self.throttle = 0
        self.time1 = time.monotonic()

    def run(self, humidity):
        while True:
            if(time.monotonic() - self.time1 > 1):
                self.time1 = time.monotonic()
                if humidity < 20:
                    self.throttle = 0
                elif humidity < 25:
                    self.throttle = 0.3
                elif humidity < 30:
                    self.throttle = 0.4
                elif humidity < 35:
                    self.throttle = 0.5
                elif humidity < 40:
                    self.throttle = 0.6
                elif humidity < 45:
                    self.throttle = 0.7
                elif humidity < 50:
                    self.throttle = 0.8
                #print("Humidity:", self.dht.humidity)
                #print("Throttle:", self.throttle)
            
            #self.motor.throttle = self.throttle
