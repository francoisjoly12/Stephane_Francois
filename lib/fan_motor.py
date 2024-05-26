#fan_motor.py
from adafruit_motor.motor import DCMotor
from pwmio import PWMOut

class fan_motor:
    def __init__(self, motor_pvm1, motor_pvm2):
        self.motor = DCMotor(PWMOut(motor_pvm1), PWMOut(motor_pvm2))
        self.throttle = 0

    def run(self, humidity, gas, obstacle):
                # gas prioritaire sur humidity
                if gas > 70:
                    self.throttle = -0.8
                elif gas > 55:
                    self.throttle = -0.7
                elif gas > 40:
                    self.throttle = -0.6
                elif gas > 25:
                    self.throttle = -0.5
                elif gas > 15:
                    self.throttle = -0.4
                    
                #humidity
                elif humidity < 40:
                    self.throttle = 0
                elif humidity < 45:
                    self.throttle = 0.4
                elif humidity < 50:
                    self.throttle = 0.5
                elif humidity < 55:
                    self.throttle = 0.6
                elif humidity < 65:
                    self.throttle = 0.7
                elif humidity > 75:
                    self.throttle = 0.8

                # gestion d'obstable  
                if obstacle:
                     self.throttle = 0

                self.motor.throttle = self.throttle

    def stop_fan(self):
         self.throttle=0
         self.motor.throttle = self.throttle

    def run_app(self, obstacle):
         self.throttle = 0.7
         
        # gestion d'obstable  
         if obstacle:
            self.throttle = 0

         self.motor.throttle = self.throttle

    def get_throttle(self):
         return self.motor.throttle
         
         
         

