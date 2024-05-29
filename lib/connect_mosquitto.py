# -----------------------------------------------------------------------------
# Script : connect_mosquitto.py
# Auteur : François Joly, Stephane_Provost
# Description : Programme de simulation d'une chambre forte avec ventillation.
#               Fonctions pour la connexion wifi et au broker mosquitto
# Date : 2024/05/27
# -----------------------------------------------------------------------------

import os
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

def connect(client, userdata, flags, rc):
    print('Connected to MQTT Broker!')
    print('Flags: {0}\n RC: {1}'.format(flags, rc))

def disconnect(client, userdata, rc):
    print('Disconnected from MQTT Broker!')

def subscribe(client, userdata, topic, granted_qos):
    print('Subscribed to {0} with QOS level {1}'.format(topic, granted_qos))

def unsubscribe(client, userdata, topic, pid):
    print('Unsubscribed from {0} with PID {1}'.format(topic, pid))

def publish(client, userdata, topic, pid):
    print('Published to {0} with PID {1}'.format(topic, pid))

def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))

    # Associez les callbacks en fonction du topic
    if topic == 'alarm':
        alarm_callback(client, topic, message)
    elif topic == 'fan_mode':
        fan_mode_callback(client, topic, message)
    elif topic == 'app_mode':
        mode_callback(client, topic, message)
    elif topic == 'door':
        door_callback(client, topic, message)

# Fonctions de rappel pour topic MQTT
def door_callback(client, topic, msg):
    global door_state
    if msg == "Up":
        door_state= True
    elif msg == "Down":
        door_state=False
    print(f"Door status updated: {door_state}")

def alarm_callback(client, topic, msg):
    global alarm_active
    global app_alarm
    if msg == "Alarme" or msg == "On":
        alarm_active = True
    else:
        alarm_active = False
    app_alarm =alarm_active
    print(f"Alarm status updated: {alarm_active}")

def fan_mode_callback(client, topic, msg):
    global fan_mode
    global fan_on
    if msg =="On" or msg =="Push" or msg == "Pull"or msg == "Bloc":
        fan_on = True
    else:
        fan_on=False
    fan_mode = msg
    print(f"Fan mode updated: {fan_mode}")

def mode_callback(client, topic, msg):
    global mode
    global switch
    mode = msg
    if mode == "Manuel":
        switch=True
    else:
        switch=False
    print(f"App mode updated: {mode}")
    
def connect_wifi():
    try:
        if os.getenv("AIO_USERNAME") and os.getenv("AIO_KEY"):
            secrets = {
                "aio_username": os.getenv("AIO_USERNAME"),
                "aio_key": os.getenv("AIO_KEY"),
                "ssid": os.getenv("CIRCUITPY_WIFI_SSID"),
                "password": os.getenv("CIRCUITPY_WIFI_PASSWORD"),
            }
        else:
            raise ImportError("Missing environment variables")
    except ImportError as e:
        print(e)
        raise

    try:
        if not wifi.radio.connected:
            print("Connecting to %s" % secrets["ssid"])
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            print("Connected to %s!" % secrets["ssid"])
    except Exception as e:
        print(f"Wi-Fi connection failed: {e}")
        raise

def connect_mqtt():
    try:
        pool = socketpool.SocketPool(wifi.radio)
        mqtt_client = MQTT.MQTT(
            broker="192.168.0.150",
            socket_pool=pool,
            port=1883,
            keep_alive=60
        )

        mqtt_client.on_connect = connect
        mqtt_client.on_disconnect = disconnect
        mqtt_client.on_subscribe = subscribe
        mqtt_client.on_unsubscribe = unsubscribe
        mqtt_client.on_publish = publish
        mqtt_client.on_message = message

        mqtt_client.connect()
        return mqtt_client
    except Exception as e:
        print(f"MQTT connection failed: {e}")
        raise

def is_mqtt_connected(mqtt_client):
    return mqtt_client.is_connected()

