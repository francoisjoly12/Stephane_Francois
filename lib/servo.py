import board
import digitalio
import time
import busio
from adafruit_motor import servo
import pwmio


#valeur pour tester ***** remplacer par Input.open, input.close et obstacle_sensor.obstacle_detected   ******** 


#https://cdn-learn.adafruit.com/downloads/pdf/using-servos-with-circuitpython.pdf


class ServoController:
    def __init__(self, servo_pin):
        pwm = pwmio.PWMOut(servo_pin, duty_cycle=2 ** 15, frequency=50)
        self.my_servo = servo.Servo(pwm)
        self.ouvrir = False
        self.fermer = False
        self.obstacle_detected = False

    def operate_servo(self):
        while True:
            if self.obstacle_detected:  #obstacle_sensor.obstacle_detected
                if self.ouvrir:
                    for angle in range(0, 180, 2):  # 0 - 180 degrees, 10 degrees at a time.
                        self.my_servo.angle = angle
                        time.sleep(0.05)
                    self.ouvrir = False
                if self.fermer:
                    for angle in range(180, 0, -2): # 180 - 0 degrees, 10 degrees at a time.
                        self.my_servo.angle = angle
                        time.sleep(0.05)
                    self.fermer = False
            else:
                if self.ouvrir:
                    for angle in range(0, 180, 8):  # 0 - 180 degrees, 10 degrees at a time.
                        self.my_servo.angle = angle
                        time.sleep(0.05)
                    self.ouvrir = False
                if self.fermer:
                    for angle in range(180, 0, -8): # 180 - 0 degrees, 10 degrees at a time.
                        self.my_servo.angle = angle
                        time.sleep(0.05)
                    self.fermer = False
