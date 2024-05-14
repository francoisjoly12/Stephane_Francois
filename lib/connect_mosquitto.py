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

def connecter_mqtt():
    try:
        if os.getenv("AIO_USERNAME") and os.getenv("AIO_KEY"):
            secrets = {
                "aio_username": os.getenv("AIO_USERNAME"),
                "aio_key": os.getenv("AIO_KEY"),
                "ssid": os.getenv("CIRCUITPY_WIFI_SSID"),
                "password": os.getenv("CIRCUITPY_WIFI_PASSWORD"),
            }
        else:
            raise ImportError("Missing environment variables for Adafruit IO credentials.")
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

    try:
        pool = socketpool.SocketPool(wifi.radio)
        mqtt_client = MQTT.MQTT(
            broker="192.168.0.150",
            socket_pool=pool,
            port=1883
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
