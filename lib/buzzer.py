import board
import digitalio
import analogio
import pwmio
import time

class BuzzerController:
    def __init__(self, buzzer_pin):
        self.buzzer = pwmio.PWMOut(buzzer_pin, variable_frequency=True, duty_cycle=2**15)
        self.time3 = time.monotonic()
        self.buzzer.frequency = 349
        self.etat = 0
        self.alarme = 1

    def run(self):
        while True:
            if self.alarme == 1:
                if (time.monotonic() - self.time3 > 0.5):
                    self.time3 = time.monotonic()
                    if self.etat == 0:
                        self.buzzer.duty_cycle = not self.buzzer.duty_cycle
                        self.etat = 1
                    else:
                        self.buzzer.duty_cycle = 2**15
                        self.etat = 0
            else:
                self.buzzer.duty_cycle = not self.buzzer.duty_cycle
