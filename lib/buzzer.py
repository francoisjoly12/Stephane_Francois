#buzzer.py
import pwmio
import time
import asyncio

class BuzzerController:
    def __init__(self, buzzer_pin):
        self.buzzer = pwmio.PWMOut(buzzer_pin, variable_frequency=True, duty_cycle=0)  
        self.buzzer.frequency = 349
        self.time_rapide = 0.2
        self.time_lente = 0.5
        self.etat = False 
        self.last_time = time.monotonic()

    def alarme_lente(self, current_time):
        if (current_time - self.last_time)>= self.time_lente:
            self.last_time = current_time
            self.buzzer.duty_cycle = 2**15 if self.etat else 0  
            self.etat = not self.etat  

    def alarme_rapide(self, current_time):
        if (current_time - self.last_time)>= self.time_rapide:
            self.last_time = current_time
            self.etat = not self.etat  
            self.buzzer.duty_cycle = 2**15 if self.etat else 0 

 
    def buzz(self, current_time):
        if (current_time - self.last_time > 0.5):
            self.last_time = current_time
            if self.etat == 0:
                self.buzzer.duty_cycle =  2**15
                self.etat = 1
            else:
                self.buzzer.duty_cycle = 0

    def off(self):
        self.buzzer.duty_cycle = not self.buzzer.duty_cycle 