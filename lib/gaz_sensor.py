import time
import math
import digitalio
import board
from analogio import AnalogIn

class GasDetector:
    def __init__(self): #buzzer_pin):
        
        self.status = 1
        self.count = 0
        self.adc = AnalogIn(board.A3)

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

           

        
#Note: Dans A3