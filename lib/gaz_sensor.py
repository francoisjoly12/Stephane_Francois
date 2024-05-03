import time
import math
import digitalio
import board
from analogio import AnalogIn

class GasDetector:
    def __init__(self, do_pin=board.IO16, buzzer_pin=board.IO10):
        self.DO = digitalio.DigitalInOut(do_pin)
        self.DO.direction = digitalio.Direction.INPUT
        self.Buzz = digitalio.DigitalInOut(buzzer_pin)
        self.Buzz.direction = digitalio.Direction.OUTPUT
        self.status = 1
        self.count = 0
        self.adc = AnalogIn(board.A0)

    def print_status(self, status):
        if status == 1:
            print ('')
            print ('   *********')
            print ('   * Safe~ *')
            print ('   *********')
            print ('')
        elif status == 0:
            print ('')
            print ('   ***************')
            print ('   * Danger Gas! *')
            print ('   ***************')
            print ('')

    def loop(self):
        while True:
            gas_value = self.adc.value
            print(gas_value)

            tmp = self.DO.value
            if tmp != self.status:
                self.print_status(tmp)
                self.status = tmp

            if self.status == 0:
                self.count += 1
                if self.count % 2 == 0:
                    self.Buzz.value = True
                else:
                    self.Buzz.value = False
            else:
                self.Buzz.value = True
                self.count = 0

            time.sleep(0.2)

    def cleanup(self):
        self.Buzz.value = True

if __name__ == '__main__':
    gas_detector = GasDetector()
    try:
        gas_detector.loop()
    except KeyboardInterrupt:
        gas_detector.cleanup()

        
#Note: Dans A3