import board
import time
import adafruit_dht
from affichage_ecran import Ecran
#from buzzer import BuzzerController
from gaz_sensor import GasDetector
#from laser import LaserDetector
from obstacle_sensor import ObstacleSensor
from fan_motor import fan_motor
#from servo import ServoController
#from sd_card import SDLogger
#from led import FlashingLED
#import asyncio

ecran = Ecran()
#buzzer = BuzzerController(board.IO10)   # Dans D5
gas_detector = GasDetector()   # Dans A3
#laser_detector = LaserDetector(transmitter_pin=board.IO9, receiver_pin=board.IO7)   # Dans D4 et D2
obstacle_sensor = ObstacleSensor(board.IO12)    # Dans D7
moteur = fan_motor(board.IO13, board.IO14)    # Dans D8 et A0 pour 5V
#servo_controller = ServoController(servo_pin=board.A1)  # Dans A1
#sd_logger = SDLogger(sd_cs_pin=board.IO15)  # Sur le top
#led = FlashingLED(board.IO11)   # D6 intégré
humidite = adafruit_dht.DHT11(board.IO8)    # D3 intégré
#sd_logger.initialize()

def main():
    last_display_time = time.monotonic()
    #alarm_timer = time.monotonic()
    
    try:
        while True:
            if time.monotonic() - last_display_time >= 0.5:
                last_display_time = time.monotonic()
                humidity = humidite.humidity
                gas_level = gas_detector.get_value()
                obstacle = obstacle_sensor.detect()
                print(obstacle)
                if(gas_level > 10):
                    fan_state = "Pull"
                elif(humidity > 40):
                    fan_state = "Push"
                else:
                    fan_state = "off"

                if(obstacle == True):
                    fan_state = "bloc"
                
                #fait tourné le moteur en fontion de l'humidité et du gas
                
                moteur.run(humidity, gas_level, obstacle)

                door_state = "Up"
                mode = "Auto"
                connection = "Off"
                ecran.refresh_text(humidity, gas_level, door_state, fan_state, mode, connection)



            
            #laser_detector.printValue()
            #alert=laser_detector.detect()
            #if alert:
            #    alarm_timer = time.monotonic()
            #    buzzer.alarme_rapide(alarm_timer)
            #    led.flash_rapide(alarm_timer)
            #else:
            #   buzzer.off()
            #   led.led.value = False

    except KeyboardInterrupt:
        pass
    except Exception as e:
            print("Une erreur est survenue :", e)

main()