# -----------------------------------------------------------------------------
# Script : main.py
# Auteur : François Joly, Stephane_Provost
# Description : Programme de simulation d'une chambre forte avec ventilation
# Date : 2024/05/27
# -----------------------------------------------------------------------------

import board
import time
import adafruit_dht
import connect_mosquitto
# Import des objets représentant les entrées/sorties
from affichage_ecran import Ecran
from buzzer import BuzzerController
from gaz_sensor import GasDetector
from laser import LaserDetector
from obstacle_sensor import ObstacleSensor
from fan_motor import fan_motor
from servo import ServoController
from sd_card import SDLogger
from led import FlashingLED

connected = False
mosquitto = False
sd_logger = None
mqtt_client = None
ecran = None
buzzer = None
gas_detector = None
laser_detector = None
obstacle_sensor = None
moteur = None
servo_controller = None
led = None
humidite = None
alarm_active = False
mode = "Auto" 
fan_speed = 0  

# Topics
mqtt_topics = {
    'gas': 'gas',
    'hum': 'hum',
    'alarm': 'alarm',
    'door': 'door',
    'fan_speed': 'fan_speed',
    'app_mode': 'app_mode',
    'fan_mode': 'fan_mode'
}

def initialize_sd_logger():
    global sd_logger
    sd_logger = SDLogger(sd_cs_pin=board.IO15)  # Sur le top
    sd_logger.initialize()

# Gestion des erreurs
# Nous avons choisi d'inclure plus de messages en console que la demande pour aider au déboguage
def handle_error(message, error=None):
    if error:
        print(message, error)
    else:
        print(message)
    if sd_logger:   # Écriture en log seulement si la carte initialisée
        sd_logger.log_data(message)

# Vérification de la présence de l'entrée/sortie pour gestion des erreurs
def check_instance(obj, cls, name):
    if isinstance(obj, cls):
        return obj
    else:
        message = f"Aucun {name} détecté."
        handle_error(message)
        return None

def connect_to_wifi():
    global connected
    try:
        connect_mosquitto.connect_wifi()
        print("Connecté au WiFi")
        connected = True
    except Exception as e:
        handle_error("Impossible de se connecter au WiFi:", e)

def connect_to_mqtt():
    global mqtt_client, mosquitto
    if connected:
        try:
            mqtt_client = connect_mosquitto.connect_mqtt()
            mosquitto = True
            print("Connecté au MQTT Broker!")
        except Exception as e:
            handle_error("Impossible de se connecter au broker MQTT:", e)
     # mosquitto -v -c "C:\Program Files\mosquitto\mosquitto.conf"      Commande de connexion au serveur mosquitto

def initialize_sensors():
    global ecran, buzzer, gas_detector, laser_detector, obstacle_sensor, moteur, servo_controller, led, humidite
    try:
        ecran = Ecran()
        ecran = check_instance(ecran, Ecran, "écran")
    except NameError as e:
        handle_error("Erreur d'écran", e)

    try:
        buzzer = BuzzerController(board.IO10)   # Dans D5
        buzzer = check_instance(buzzer, BuzzerController, "Buzzer")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de buzzer", e)

    try:
        gas_detector = GasDetector(board.A4)   # Dans A4
        gas_detector = check_instance(gas_detector, GasDetector, "gas detector")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de gas detector", e)

    try:
        laser_detector = LaserDetector(transmitter_pin=board.IO9, receiver_pin=board.IO7)   # Dans D4 et D2
        laser_detector = check_instance(laser_detector, LaserDetector, "capteur laser")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de laser", e)

    try:
        obstacle_sensor = ObstacleSensor(board.IO12)    # Dans D7
        obstacle_sensor = check_instance(obstacle_sensor, ObstacleSensor, "capteur d'obstacle")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur d'obstacle sensor", e)
    
    try:
        moteur = fan_motor(board.IO13, board.IO14)    # Dans D8 et A0 pour 5V
        moteur = check_instance(moteur, fan_motor, "moteur")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de fan motor", e)

    try:
        servo_controller = ServoController(servo_pin=board.A1)  # Dans A1
        servo_controller = check_instance(servo_controller, ServoController, "Servo")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de servomoteur", e)
    
    try:
        led = FlashingLED(board.IO11)   # D6 intégré
        led = check_instance(led, FlashingLED, "LED")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de LED", e)

    try:
        humidite = adafruit_dht.DHT11(board.IO8)    # D3 intégré
        humidite = check_instance(humidite, adafruit_dht.DHT11, "capteur DHT")
    except (NameError, RuntimeError) as e:
        handle_error("Erreur de DHT", e)

def subscribe_to_topics():
    global mqtt_client, mosquitto,  mqtt_topics    
    # Seulement si connecté au broker
    if mosquitto:
        for topic in mqtt_topics.values():
            mqtt_client.subscribe(topic, qos=1)

def publish_topics(gas_level, humidity, alarm_mqtt, fan_state, fan_speed, door_state):
    global connected, mosquitto, mqtt_topics, led, buzzer, gas_detector, humidite, moteur
    # Seulement si connecté au broker
    if connected and mosquitto:
        try:
            if gas_detector:
                mqtt_client.publish(mqtt_topics['gas'], gas_level, qos=1)
            if humidite:
                mqtt_client.publish(mqtt_topics['hum'], humidity)
            if led and buzzer:
                mqtt_client.publish(mqtt_topics['alarm'], alarm_mqtt)
            if moteur:
                mqtt_client.publish(mqtt_topics['fan_mode'], fan_state)
                mqtt_client.publish(mqtt_topics['fan_speed'], fan_speed)
            if servo_controller:
                mqtt_client.publish(mqtt_topics['door'], door_state)
            
        except Exception as e:
            handle_error("Erreur lors de la publication MQTT:", e)
            connected = False
            mosquitto = False

# Programme en mode automatique
def run_auto(humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt):
    global mosquitto, mqtt_topics, sd_logger, alarm_active, connected
    global ecran, buzzer, gas_detector, laser_detector, obstacle_sensor, moteur, servo_controller, led, humidite

    try:
        # Vérification si l'alarme est déclenchée actuellement
        if alarm_active:
            alarm_mqtt = "Alarme"
        else:
            alarm_mqtt = ""

        # Opération de la fan
        if moteur:
            obstacle = obstacle_sensor.detect()
            moteur.run(humidity, gas_level, obstacle)
            fan_state = (
                "Pull" if moteur.throttle < 0 else
                "Push" if moteur.throttle > 0 else
                "Off"
            )
            if obstacle:
                fan_state = "Bloc"
            
            fan_speed = moteur.throttle

        # Fermeture de porte suite à la détection du vol
        if laser_detector and servo_controller:
            alert = laser_detector.detect()
            if alert:
                alarm_active = True                
                if servo_controller.get_current_angle() < 0:
                    door_state = "Down"
                    servo_controller.close_door()
                fin_alarm_timer = time.monotonic()
            elif not alarm_active and servo_controller.get_current_angle() > 0:
                door_state = "Up"
                servo_controller.open_door() 

        # Alarme led et buzzer lors de la détection du vol
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
            if led:
                led.led.value = False

        # Publish des données  
        publish_topics(gas_level, humidity, alarm_mqtt, fan_state, fan_speed, door_state)

        return humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Une erreur est survenue :", e)

# Exécution du programme en mode manuel
def run_manual_mode(connect_mosquitto, humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt):
    mode = "Man"
    subscribe_to_topics()
    
    # Gestion de l'alarme
    if connect_mosquitto.app_alarm:
        alarm_mqtt = "Alarme"
        led.flash_rapide(time.monotonic())
        buzzer.alarme_rapide(time.monotonic())
    else:
        alarm_mqtt = ""
        buzzer.off()
        led.stop_led()

    # Gestion du ventilateur
    if connect_mosquitto.fan_on:
        obstacle = obstacle_sensor.detect()
        moteur.run(humidity, gas_level, obstacle)
        fan_state = (
                "Pull" if moteur.throttle < 0 else
                "Push" if moteur.throttle > 0 else
                "Off"
            )
        if obstacle:
            fan_state = "Bloc"
        fan_speed = moteur.get_throttle()
    else:
        moteur.stop_fan()
        fan_state = "Off"
        fan_speed = 0

    # Gestion de la porte
    if connect_mosquitto.door_state:
        door_state = "Up"
        servo_controller.open_door()
    else:
        door_state = "Down"
        servo_controller.close_door()

    publish_topics(gas_level, humidity, alarm_mqtt, fan_state, fan_speed, door_state)

    return humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt


def main():
    global mosquitto, mqtt_topics, sd_logger, alarm_active, connected
    global ecran, buzzer, gas_detector, laser_detector, obstacle_sensor, moteur, servo_controller, led, humidite

    initialize_sd_logger()
    connect_to_wifi()
    connect_to_mqtt()
    initialize_sensors()
    subscribe_to_topics()

    # Variables de temps
    last_display_time = time.monotonic()
    last_detect_time = time.monotonic()
    fin_alarm_timer = time.monotonic()
   
    # Première valeur des capteurs
    if humidite:
        humidity = humidite.humidity
    else:
        humidity = 'N/A'
    if gas_detector:
        gas_level = gas_detector.get_value()
    else:
        gas_level = 'N/A'
    
    # États
    alarm_mqtt = ""
    door_state = "Up"
    fan_state = "Off"
    if mosquitto:
        connection = "On"
    else:
        connection = "Off"
    connect_mosquitto.switch=False
    
    # Boucle principale
    try:
        while True:
            # Prise de données
            if time.monotonic() - last_detect_time >= 1:
                last_detect_time = time.monotonic()
                if humidite:
                    humidity = humidite.humidity
                if gas_detector:
                    gas_level = gas_detector.get_value()
            
            try:
                # Vérification de la connexion MQTT
                if mqtt_client and not connect_mosquitto.is_mqtt_connected(mqtt_client):
                    sd_logger.log_data("Perte de connexion MQTT")
                    mqtt_client.connect()
                    if connect_mosquitto.is_mqtt_connected(mqtt_client):
                        sd_logger.log_data("Rétablissement de la connexion MQTT")
            except Exception as e:
                handle_error("Une erreur est survenue :", e)
            
            # Switch entre mode auto et manuel
            if not connect_mosquitto.switch:
                mode = "Auto"
                humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt = run_auto(
                    humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt
                )
            else:
                humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt = run_manual_mode(
                    connect_mosquitto, humidity, gas_level, door_state, fan_state, mode, connection, last_detect_time, fin_alarm_timer, alarm_mqtt
                )
                        
            # Affichage de l'écran  
            if time.monotonic() - last_display_time >= 0.5:
                last_display_time = time.monotonic()
                if ecran:
                    ecran.refresh_text(humidity, gas_level, door_state, fan_state, mode, connection)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Une erreur est survenue :", e)

main()

