#fan_motor.py
import board
import time
from adafruit_motor.motor import DCMotor
from pwmio import PWMOut

class fan_motor:
    def __init__(self, motor_pvm1, motor_pvm2):
        self.motor = DCMotor(PWMOut(motor_pvm1), PWMOut(motor_pvm2))
        self.throttle = 0
        #self.time1 = time.monotonic()

    def run(self, humidity, gas, obstacle):
        #while True:
            #if(time.monotonic() - self.time1 > 1):
                #self.time1 = time.monotonic()
                
                #print("humidity", humidity)
                #print("gas",  gas)
                
                if gas > 10:
                    self.throttle = -0.8
                elif humidity < 40:
                    self.throttle = 0
                elif humidity < 45:
                    self.throttle = 0.5
                elif humidity < 50:
                    self.throttle = 0.6
                elif humidity < 55:
                    self.throttle = 0.7
                elif humidity > 55:
                    self.throttle = 0.8
                    
                if obstacle:
                     self.throttle = 0

                self.motor.throttle = self.throttle
                return self.throttle

                #print("throttle", self.throttle)
                #print("Humidity:", self.dht.humidity)
                #print("Throttle:", self.throttle)


