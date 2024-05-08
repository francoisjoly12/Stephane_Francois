#servo.py
import time
from adafruit_motor import servo
import pwmio
import asyncio


#https://cdn-learn.adafruit.com/downloads/pdf/using-servos-with-circuitpython.pdf

class ServoController:
    def __init__(self, servo_pin):
        pwm = pwmio.PWMOut(servo_pin, duty_cycle=2 ** 15, frequency=50, )
        self.my_servo = servo.Servo(pwm)
        self.angle_step = 2  # Pas de changement d'angle
        self.time_step = 0.05  # Temps entre chaque pas
        self.last_time = time.monotonic()
        self.temps_rapide = 0.2  
        self.temps_lent = 0.5  
        self.my_servo.angle=0
        self.current_angle = 180  # Angle actuel du servo

    def open_door(self):
        # Ouvrir progressivement la porte
        if self.current_angle > 0:
            while self.current_angle > 0:
                current_time = time.monotonic()
                if current_time - self.last_time >= self.time_step:
                    self.last_time = current_time
                    self.current_angle -= self.angle_step
                    if self.current_angle < 0:
                        self.current_angle = 0  # Limiter l'angle à 0 degrés
                    self.my_servo.angle = self.current_angle
        else:
            # Si la porte est déjà complètement ouverte, ne rien faire
            pass

    def close_door(self):
        # Fermer progressivement la porte
        if self.current_angle < 180:
            while self.current_angle < 180:
                current_time = time.monotonic()
                if current_time - self.last_time >= self.time_step:
                    self.last_time = current_time
                    self.current_angle += self.angle_step
                    if self.current_angle > 180:
                        self.current_angle = 180  # Limiter l'angle à 180 degrés
                    self.my_servo.angle = 0
    
    def move_door(self, current_time):
        self.current_angle= self.my_servo.angle
        if self.current_angle < 0:
            target_angle = 180  # Si la porte est fermée, l'ouvrir
        else:
            target_angle = 0  # Sinon, la fermer

       
        while self.current_angle != target_angle:
            #current_time = time.monotonic()
            if  (current_time - self.last_time) >= self.temps_lent:
                self.last_time = current_time
                if self.current_angle < target_angle:
                    self.current_angle += self.angle_step
                else:
                    self.current_angle -= self.angle_step

                if self.current_angle > 180:
                    self.current_angle = 180  
                elif self.current_angle < 0:
                    self.current_angle = 0  

                #self.my_servo.angle = self.current_angle

    def get_current_angle(self):
        return self.my_servo.angle
    
    def set_angle(self, angle):
        self.my_servo.angle=angle

async def close_door_async(self):
        # Fermer progressivement la porte
        while self.current_angle < 180:
            current_time = time.monotonic()
            if current_time - self.last_time >= self.time_step:
                self.last_time = current_time
                self.current_angle += self.angle_step
                if self.current_angle > 180:
                    self.current_angle = 180  # Limiter l'angle à 180 degrés
                self.my_servo.angle = self.current_angle
                await asyncio.sleep(0)  # Attendre un peu pour ne pas bloquer le reste du programme