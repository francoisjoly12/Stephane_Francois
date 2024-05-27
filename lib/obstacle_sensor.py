# -----------------------------------------------------------------------------
# Script : buzzer.py
# Auteur : François Joly, Stephane_Provost
# Description : Programme de simulation d'une chambre forte avec ventillation.
#               Objet ObstacleSensor
# Date : 2024/05/27
# -----------------------------------------------------------------------------

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