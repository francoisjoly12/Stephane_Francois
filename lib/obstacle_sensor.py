import digitalio

class ObstacleSensor:
    def __init__(self, pin):
        self.pin = pin
        self.sensor = digitalio.DigitalInOut(pin)
        self.sensor.direction = digitalio.Direction.INPUT
        self.sensor.pull = digitalio.Pull.UP

    def detect(self):
        if not self.sensor.value:
            print("Obstacle détecté!")
            return not self.sensor.value