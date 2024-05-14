#connect_mosquitto.py
import os
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT


def connect(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print('Connected to MQTT Broker!')
    print('Flags: {0}\n RC: {1}'.format(flags, rc))

def disconnect(client, userdata, rc):
    # This method is called when the client disconnects
    # from the broker.
    print('Disconnected from MQTT Broker!')

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QOS level {1}'.format(topic, granted_qos))

def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a feed.
    print('Unsubscribed from {0} with PID {1}'.format(topic, pid))

def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a feed.
    print('Published to {0} with PID {1}'.format(topic, pid))

def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))

def connecter_mqtt():
    # Connexion au WIFI à partir des informations de settings.toml

    try:
        if os.getenv("AIO_USERNAME") and os.getenv("AIO_KEY"):
            secrets = {
                "aio_username": os.getenv("AIO_USERNAME"),
                "aio_key": os.getenv("AIO_KEY"),
                "ssid": os.getenv("CIRCUITPY_WIFI_SSID"),
                "password": os.getenv("CIRCUITPY_WIFI_PASSWORD"),
            }
        else:
            raise ImportError
    except ImportError:
        print(
            "Les informations pour la connexion au WIFI et pour Adafruit IO ne sont pas disponibles dans le fichier settings.toml")
        raise


    if not wifi.radio.connected:
        print("Connexion à %s" % secrets["ssid"])
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("Connecté à %s!" % secrets["ssid"])
    
   
    pool = socketpool.SocketPool(wifi.radio)
    
    mqtt_client = MQTT.MQTT(
        broker="10.170.51.21",
        socket_pool=pool,
        port=1883
        )

    # Connect callback handlers to mqtt_client
    mqtt_client.on_connect = connect
    mqtt_client.on_disconnect = disconnect
    mqtt_client.on_subscribe = subscribe
    mqtt_client.on_unsubscribe = unsubscribe
    mqtt_client.on_publish = publish
    mqtt_client.on_message = message
   
    mqtt_client.connect()
    return mqtt_client

