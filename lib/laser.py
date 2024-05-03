import time
import board
import digitalio

class LaserDetector:
    def __init__(self, transmitter_pin, receiver_pin):
        self.transmitter_pin = digitalio.DigitalInOut(transmitter_pin)
        self.transmitter_pin.direction = digitalio.Direction.OUTPUT
        self.transmitter_pin.value = True
        
        self.receiver_pin = digitalio.DigitalInOut(receiver_pin)
        self.receiver_pin.direction = digitalio.Direction.INPUT
        
    def alert(self):
        print("Alerte! Quelqu'un passe devant le laser.")
        
    def detect(self):
        current_time = time.monotonic()
        if current_time - self.last_display_time > 0.5:
            self.last_display_time = current_time
            if not self.receiver_pin.value:  
                self.alert()

transmitter_pin = board.IO13
receiver_pin = board.IO14

laser_detector = LaserDetector(transmitter_pin, receiver_pin)
laser_detector.last_display_time = time.monotonic()

while True:
    laser_detector.detect()


#Note:  trasmitter D4 receiver D3