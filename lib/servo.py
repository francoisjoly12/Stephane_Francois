#servo.py
from adafruit_motor import servo
import pwmio

class ServoController:
    def __init__(self, servo_pin):
        pwm = pwmio.PWMOut(servo_pin, duty_cycle=2 ** 15, frequency=50, )
        self.my_servo = servo.Servo(pwm)
        self.my_servo.angle=0
        

    def close_door(self):
        for angle in range(180, 0, -5): 
            while self.my_servo.angle <178:
                self.my_servo.angle = angle
        print("open door")
        
    def open_door(self):
        for angle in range(0, 180, 5):
                while self.my_servo.angle >178:
                    self.my_servo.angle = angle
        print("close door")

    def get_current_angle(self):
        return self.my_servo.angle
    
