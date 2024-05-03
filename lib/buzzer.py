#buzzer.py
import pwmio
import time
import asyncio

class BuzzerController:
    def __init__(self, buzzer_pin):
        self.buzzer = pwmio.PWMOut(buzzer_pin, variable_frequency=True, duty_cycle=0)  
        self.buzzer.frequency = 349
        self.time_rapide = time.monotonic()
        self.time_lente = time.monotonic()
        self.etat = False 
        self.time3 = time.monotonic()

    async def alarme_lente(self, current_time):
        if (current_time - self.time_lente > 1):
            self.time_lente = time.monotonic()
            self.buzzer.duty_cycle = 0xFFFF if self.etat else 0  
            self.etat = not self.etat  

    async def alarme_rapide(self, current_time):
        if (current_time - self.time_rapide > 0.5):
            self.time_rapide = time.monotonic()
            self.etat = not self.etat  
            self.buzzer.duty_cycle = 0xFFFF if self.etat else 0 

    async def off(self):
        self.buzzer.duty_cycle = 0

    async def buzz(self, current_time):
        if (current_time - self.time3 > 0.5):
            self.time3 = current_time
            if self.etat == 0:
                self.buzzer.duty_cycle =  2**15
                self.etat = 1
            else:
                self.buzzer.duty_cycle = 0

    async def alarme_lente(self, time):
        if (time - self.time_lente > 1):
            self.time_lente = time.monotonic()
            self.buzzer.duty_cycle = 0xFFFF if self.etat else 0  
            self.etat = not self.etat  

    async def alarme_rapide(self, time):
        if (time - self.time_rapide > 0.5):
            self.time_rapide = time.monotonic()
            self.etat = not self.etat  
            self.buzzer.duty_cycle = 0xFFFF if self.etat else 0 

    def off(self):
        self.buzzer.duty_cycle = not self.buzzer.duty_cycle 

    def off(self):
        self.buzzer.duty_cycle = 0
     