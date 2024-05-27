# -----------------------------------------------------------------------------
# Script : buzzer.py
# Auteur : François Joly, Stephane_Provost
# Description : Programme de simulation d'une chambre forte avec ventillation.
#               Objet GasDetector
# Date : 2024/05/27
# -----------------------------------------------------------------------------

from analogio import AnalogIn

class GasDetector:
    def __init__(self, sensor_pin): 
        self.count = 0
        self.adc = AnalogIn(sensor_pin)

    def get_value(self):
        #-5000 pour avoir une valeur ambiante proche de 0% et (100 / 47600) pour avoir une valeur en pourcentage en fontion du range.
        gas_value = ((self.adc.value - 5400) * 100 / 47600)
        # Empêche d'afficher des valeur négative
        if(gas_value < 0):
            gas_value = 0
        return gas_value
