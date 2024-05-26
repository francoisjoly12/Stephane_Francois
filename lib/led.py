#led.py
import digitalio
import time

class FlashingLED:
    def __init__(self, led_pin):
        self.led = digitalio.DigitalInOut(led_pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self.etat = False  
        self.temps_rapide = 0.2  
        self.temps_lent = 0.5  
        self.last_time = time.monotonic()

    def flash_rapide(self, current_time):
        if (current_time - self.last_time) >= self.temps_rapide:
            self.last_time = current_time
            self.etat = not self.etat
            self.led.value = self.etat

    def flash_lent(self):
        if (time.monotonic() - self.last_time) >= self.temps_lent:
            self.last_time = time.monotonic()
            self.etat = not self.etat
            self.led.value = self.etat
