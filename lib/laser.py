# laser.py
import digitalio

class LaserDetector:
    def __init__(self, transmitter_pin, receiver_pin):
        self.transmitter_pin = digitalio.DigitalInOut(transmitter_pin)
        self.transmitter_pin.direction = digitalio.Direction.OUTPUT
        self.transmitter_pin.value = True
        self.receiver_pin = digitalio.DigitalInOut(receiver_pin)
        self.receiver_pin.direction = digitalio.Direction.INPUT
        
    def alert(self):
        print("Alerte! L'objet de valeur à été volé.")
        
    def detect(self):
        if self.receiver_pin.value:  
                self.alert()
                return True