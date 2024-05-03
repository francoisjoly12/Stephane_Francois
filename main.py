import board
import time
import adafruit_dht
from affichage_ecran import Ecran
from buzzer import BuzzerController
from gaz_sensor import GasDetector
from laser import LaserDetector
from obstacle_sensor import ObstacleSensor
from motor import motor
from servo import ServoController
from sd_card import SDLogger
from led import FlashingLED
import asyncio

ecran = Ecran()
buzzer = BuzzerController(board.IO10)
gas_detector = GasDetector()
laser_detector = LaserDetector(transmitter_pin=board.IO7, receiver_pin=board.IO9)
obstacle_sensor = ObstacleSensor(board.IO12)
moteur = motor(motor_pvm1=board.IO13, motor_pvm2=board.IO14)
servo_controller = ServoController(servo_pin=board.A1)
sd_logger = SDLogger(sd_cs_pin=board.IO15)
led = FlashingLED(board.IO11)
humidite = adafruit_dht.DHT11(board.IO8)
sd_logger.initialize()

async def main():
    last_display_time = time.monotonic()
    alarm_timer = time.monotonic()
    
    try:
        while True:
            if time.monotonic() - last_display_time >= 0.5:
                last_display_time = time.monotonic()
                humidity = humidite.humidity
                gas_level = 100.0
                door_state = "Up"
                fan_state = "On"
                mode = "Automatique"
                connection = "Off"
                ecran.refresh_text(humidity, gas_level, door_state, fan_state, mode, connection)

            if obstacle_sensor.detect():
                alarm_timer = time.monotonic()
                buzzer.buzz(alarm_timer)
                led.flash_rapide(alarm_timer)
            else:
                buzzer.off()
                led.led.value = False

    except KeyboardInterrupt:
        pass


asyncio.run(main())