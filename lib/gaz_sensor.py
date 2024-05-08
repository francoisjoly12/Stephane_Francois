#gas_sensor.py
import time
import math
import digitalio
import board
from analogio import AnalogIn

class GasDetector:
    def __init__(self): 
        
        #self.status = 1
        self.count = 0
        self.adc = AnalogIn(board.A4)

    # def print_status(self, status):
    #     if status == 1:
    #         print ('')
    #         print ('   *********')
    #         print ('   * Safe~ *')
    #         print ('   *********')
    #         print ('')
    #     elif status == 0:
    #         print ('')
    #         print ('   ***************')
    #         print ('   * Danger Gas! *')
    #         print ('   ***************')
    #         print ('')

    # def loop(self):
    #     while True:
    #         gas_value = self.adc.value
    #         print(v)

    def get_value(self):
        #-5000 pour avoir une valeur ambiante proche de 0% et (100 / 47600) pour avoir une valeur en pourcentage en fontion du range.
        gas_value = ((self.adc.value - 5400) * 100 / 47600)
        #empêche d'afficher des valeur négative
        if(gas_value < 0):
            gas_value = 0
        return gas_value

#Note: Dans A3 ne pas brancher le brun/jaune