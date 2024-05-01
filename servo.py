import board
import digitalio
import time
import busio
from adafruit_motor import servo
import pwmio


#valeur pour tester ***** remplacer par Input.open, input.close et obstacle_sensor.obstacle_detected   ******** 
ouvrir = 0
fermer = 1
obstacle_detected = 1

pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

#https://cdn-learn.adafruit.com/downloads/pdf/using-servos-with-circuitpython.pdf
while True:
    if obstacle_detected == 1: #obstacle_sensor.obstacle_detected
        if ouvrir == 1:
            for angle in range(0, 180, 2): # 0 - 180 degrees, 10 degrees at a time.
                my_servo.angle = angle
                time.sleep(0.05)
            ouvrir = 0
        if fermer == 1:
            for angle in range(180, 0, -2): # 180 - 0 degrees, 10 degrees at a time.
                my_servo.angle = angle
                time.sleep(0.05)
            fermer = 0
    else:
        if ouvrir == 1:
            for angle in range(0, 180, 8): # 0 - 180 degrees, 10 degrees at a time.
                my_servo.angle = angle
                time.sleep(0.05)
            ouvrir = 0
        if fermer == 1:
            for angle in range(180, 0, -8): # 180 - 0 degrees, 10 degrees at a time.
                my_servo.angle = angle
                time.sleep(0.05)
            fermer = 0