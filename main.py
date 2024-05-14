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
import connect_mosquitto

ecran = Ecran()
buzzer = BuzzerController(board.IO10)   # Dans D5
gas_detector = GasDetector()    # Dans A3
laser_detector = LaserDetector(transmitter_pin=board.IO9, receiver_pin=board.IO7)   # Dans D4 et D2
obstacle_sensor = ObstacleSensor(board.IO12)    # Dans D7
moteur = motor(motor_pvm1=board.IO13, motor_pvm2=board.IO14)    # Dans D8 et A0 pour 5V
servo_controller = ServoController(servo_pin=board.A1)  # Dans A1
sd_logger = SDLogger(sd_cs_pin=board.IO15)  # Sur le top
led = FlashingLED(board.IO11)   # D6 intégré
humidite = adafruit_dht.DHT11(board.IO8)    # D3 intégré
sd_logger.initialize()


def main():
    #variables de temps et d'état
    last_display_time = time.monotonic()
    last_detect_time = time.monotonic()
    fin_alarm_timer = time.monotonic()
    alarm_active = False
    humidity = humidite.humidity
    #gas_level = gas_detector.get_value()
    door_state = "Up"
    fan_state = "Off"
    mode = "Auto"
    connection = "On"
    gas_level = 0
    connected =False

    #Connection à MQTT
    try:
        mqtt_client = connect_mosquitto.connecter_mqtt()  # mosquitto -v -c "C:\Program Files\mosquitto\mosquitto.conf"
        mqtt_topic_gas = 'gas'
        mqtt_topic_hum = 'hum'
        mqtt_topic_alarm = 'alarm'
        mqtt_client.subscribe(mqtt_topic_gas)
        mqtt_client.subscribe(mqtt_topic_hum)
        mqtt_client.subscribe(mqtt_topic_alarm)
        connected = True
        connection = "On"
    except Exception as e:
        print("Erreur de connexion MQTT:", e)
        connected = False
        connection = "Off"
    # Boucle principale
    try:
        while True:
            if time.monotonic() - last_detect_time >= 1:
                last_detect_time = time.monotonic()
                humidity = humidite.humidity
                #gas_level = gas_detector.get_value()
                
                #Opération de la fan
                #obstacle = obstacle_sensor.detect()
                #moteur.run(humidity, gas_level, obstacle)

                #if(gas_level > 10):
                #    fan_state = "Pull"
                #elif(humidity > 40):
                #    fan_state = "Push"
                #else:
                #    fan_state = "Off"

                #Alarme de détection de vol
                alert = laser_detector.detect()
                if alert:
                    alarm_active = True                
                    if servo_controller.get_current_angle() < 0:
                        door_state = "Down"
                        servo_controller.close_door()
                    fin_alarm_timer = time.monotonic()  

                if alarm_active:
                    led.flash_rapide(time.monotonic())
                    buzzer.alarme_rapide(time.monotonic())
                    if time.monotonic() - fin_alarm_timer >= 10:
                        buzzer.off()
                        led.led.value = False
                        servo_controller.open_door()
                        door_state = "Up"
                        alarm_active = False  
                    
                else:
                    buzzer.off()
                    led.led.value = False

                # Publish des données  
                if connected:
                    try:
                        #mqtt_client.publish(mqtt_topic_gas, gas_level)
                        mqtt_client.publish(mqtt_topic_hum, humidity)
                        #mqtt_client.publish(mqtt_topic_alarm, "active" if alarm_active else "inactive")
                    except Exception as e:
                        print("Erreur lors de la publication MQTT:", e)
                        connected = False  
                        connection = "Off"
                
            #Affichage de l'écran  
            if time.monotonic() - last_display_time >= 0.5:
                last_display_time = time.monotonic()
                ecran.refresh_text(humidity, gas_level, door_state, fan_state, mode, connection)
            
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Une erreur est survenue :", e)

main()
