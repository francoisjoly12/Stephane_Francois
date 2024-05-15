import board
import time
import adafruit_dht
from affichage_ecran import Ecran
from buzzer import BuzzerController
from gaz_sensor import GasDetector
from laser import LaserDetector
from obstacle_sensor import ObstacleSensor
from fan_motor import fan_motor
from servo import ServoController
from sd_card import SDLogger
from led import FlashingLED
import connect_mosquitto

# Initialisation des entrées et sorties
try:
    ecran = Ecran()
except Exception as e:
    print("Aucun ecran détecté.")
    ecran=None
try:
    buzzer = BuzzerController(board.IO10)   # Dans D5
except Exception as e:
    print("Aucun Buzzer détecté.")
    buzzer=None
try:
    gas_detector = GasDetector(board.A3)   # Dans A3
except Exception as e:
    print("Aucun gas detector détecté.")
    gas_detector =None
try:
    laser_detector = LaserDetector(transmitter_pin=board.IO9, receiver_pin=board.IO7)   # Dans D4 et D2
except Exception as e:
    print("Aucun capteur laser détecté.")
    laser_detector =None
try:
    obstacle_sensor = ObstacleSensor(board.IO12)    # Dans D7
except Exception as e:
    print("Aucun capteur d'obstacle détecté.")
    obstacle_sensor =None
try:
    moteur = fan_motor(motor_pvm1=board.IO13, motor_pvm2=board.IO14)    # Dans D8 et A0 pour 5V
except Exception as e:
    print("Aucun moteur détecté.")
    moteur =None
try:
    servo_controller = ServoController(servo_pin=board.A1)  # Dans A1
except Exception as e:
    print("Aucun Servo détecté.")
    servo_controller =None
try:
    led = FlashingLED(board.IO11)   # D6 intégré
except Exception as e:
    print("Aucun LED détecté.")
    led =None
try:
    humidite = adafruit_dht.DHT11(board.IO8)    # D3 intégré
except Exception as e:
    print("Aucun capteur DHT détecté.")
    humidity =None
sd_logger = SDLogger(sd_cs_pin=board.IO15)  # Sur le top
sd_logger.initialize()


def main():
   #variables de temps et d'état
    last_display_time = time.monotonic()
    last_detect_time = time.monotonic()
    fin_alarm_timer = time.monotonic()
    alarm_active = False
    # Capteurs
    if humidite:
        humidity = humidite.humidity
    if gas_detector:
        gas_level = gas_detector.get_value()
    #États
    door_state = "Up"
    fan_state = "Off"
    mode = "Auto"
    connection = "On"
    gas_level = 0
    connected =False

    #Connection à MQTT
    try:
        mqtt_client = connect_mosquitto.connecter_mqtt()  # mosquitto -v -c "C:\Program Files\mosquitto\mosquitto.conf"
        #Topics
        mqtt_topic_gas = 'gas'
        mqtt_topic_hum = 'hum'
        mqtt_topic_alarm = 'alarm'
        mqtt_topic_door= 'door'
        mqtt_topic_fan= 'fan'
        #Subscribe
        if humidite:
            mqtt_client.subscribe(mqtt_topic_hum)
        if gas_detector:
            mqtt_client.subscribe(mqtt_topic_gas)
        if alarm_active:
            mqtt_client.subscribe(mqtt_topic_alarm)
        if moteur:
            mqtt_client.subscribe(mqtt_topic_door)
        if laser_detector and servo_controller:
            mqtt_client.subscribe(mqtt_topic_fan)
        
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
                if humidite:
                    humidity = humidite.humidity
                if gas_detector:
                    gas_level = gas_detector.get_value()
                
                #Opération de la fan
                if moteur:
                    obstacle = obstacle_sensor.detect()
                    moteur.run(humidity, gas_level, obstacle)
                    if(gas_level > 10):
                        fan_state = "Pull"
                    elif(humidity > 40):
                        fan_state = "Push"
                    else:
                        fan_state = "Off"

                # Fermeture de porte suite à la détection du vol
                if laser_detector and servo_controller:
                    alert = laser_detector.detect()
                    if alert:
                        alarm_active = True                
                        if servo_controller.get_current_angle() < 0:
                            door_state = "Down"
                            servo_controller.close_door()
                        fin_alarm_timer = time.monotonic()  
                # Alarme led et buzzer
                if alarm_active and led and buzzer:
                    led.flash_rapide(time.monotonic())
                    buzzer.alarme_rapide(time.monotonic())
                    # Retour à la normale après x temps (10 secondes)
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
                        if gas_detector:
                            mqtt_client.publish(mqtt_topic_gas, gas_level)
                        if humidite:
                            mqtt_client.publish(mqtt_topic_hum, humidity)
                        if alarm_active:
                            mqtt_client.publish(mqtt_topic_alarm, "Alarme")
                        if moteur:
                            mqtt_client.publish(mqtt_topic_fan, fan_state)
                        if laser_detector and servo_controller:
                             mqtt_client.publish(mqtt_topic_door, door_state)   
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
