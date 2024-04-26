import time
import board
import digitalio

class ObstacleSensor:
    def __init__(self, pin):
        self.pin = pin
        self.sensor = digitalio.DigitalInOut(pin)
        self.sensor.direction = digitalio.Direction.INPUT
        self.sensor.pull = digitalio.Pull.UP

    def obstacle_detected(self):
        return not self.sensor.value

def main():
    obstacle_sensor = ObstacleSensor(board.IO16)  # Utilisation de la broche D11
    
    
    try:
        time1 = time.monotonic()

        while True:
            if(time.monotonic() - time1 > 1):
                time1 = time.monotonic()
                if obstacle_sensor.obstacle_detected():
                    print("Barrier detected!")
                    
    except KeyboardInterrupt:
        pass  # Ignorez l'exception KeyboardInterrupt et terminez le programme proprement

if __name__ == "__main__":
    main()


#Note : brancher rouge 5v, noir ground, jaune D11(IO16) dans l'exemple.
# Le tout fonctionne bien.
# Source https://github.com/hipi-io/HiPi-Sensor-kit-v4.0/blob/main/Python/29_ir_obstacle.py
# modifié et adapté en classe par moi-même