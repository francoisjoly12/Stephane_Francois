import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import os
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time
import adafruit_bmp280
import pcf8523
import adafruit_dht


class ecran:

    def __init__(self):
        displayio.release_displays()
        self.i2c = board.I2C()
        self.display_bus = displayio.I2CDisplay(self.i2c, device_address=0x3C)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64, rotation=180)
        self.splash = displayio.Group()
        self.display.root_group = self.splash

        self.text = ""
        self.text_area = label.Label(terminalio.FONT, text=self.text, color=0xFFFFFF, x=5, y=10)
        self.splash.append(self.text_area)

    def rafraichir_texte(self, texte):
        self.text_area.text = texte
        self.display.refresh()

    @property
    def texte(self):
        return self.text_area.text

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


# Mise en place des objets de la carte Arduino
i2c = board.I2C()
rtc = pcf8523.PCF8523(i2c)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1016.10
led = digitalio.DigitalInOut(board.IO11)
led.direction = digitalio.Direction.OUTPUT
ecran = projet2.ecran()
dht_pin = board.IO8
dht = adafruit_dht.DHT11(dht_pin)



# Variables de temps
last_display_time = time.monotonic()
last_measurement_time = time.monotonic()
print_time = None
last_time = time.monotonic()
led_last_time = time.monotonic()
# Variables de température
temp_actuelle: float = dht.temperature
temp_max: float = temp_actuelle
hum_actuelle = dht.humidity
hum_max: float = hum_actuelle

mqtt_topic_temp='temps'
mqtt_topic_hum='hum'
mqtt_client=projet2.connecter_mqtt()  
mqtt_client.subscribe(mqtt_topic_temp)
mqtt_client.subscribe(mqtt_topic_hum)
##compteurs
temp_max_flash_count = 0
hum_max_flash_count = 0

def flash(count, flash):
    if count <= flash:
        led.value = True  
        time.sleep(0.2)
        led.value = False 
        time.sleep(0.2)
    elif count > flash:
        led.value = False 

while True:
    
    if time.monotonic() - led_last_time > 2.5:
        mqtt_client.publish(mqtt_topic_temp, temp_actuelle)
        mqtt_client.publish(mqtt_topic_hum, hum_actuelle)
        temp_max = max(temp_max, temp_actuelle)
        hum_max_min = min(hum_max, hum_actuelle)
        led.value = not led.value
        led_last_time = time.monotonic()
        time.sleep(0.5)
        #print(temp_actuelle)
        # température maximale
        if temp_actuelle == temp_max:
            temp_max_flash_count += 1
            flash(temp_max_flash_count,2)

        # l'humidité maximale
        if hum_actuelle == hum_max:
            hum_max_flash_count += 1
            flash(hum_max_flash_count,3)
            
        #  les deux, température et humidité maximales 
        if temp_actuelle == temp_max and hum_actuelle == hum_max:
            led.value = True

        # Réinitialisation des compteurs
        if temp_actuelle < temp_max:
            temp_max_flash_count = 0
        if hum_actuelle < hum_max:
            hum_max_flash_count = 0
        
        ecran.rafraichir_texte(
                "Température\nactuelle:{:.1f}C\nMax{:.1f}%\nHum:{:.1f}C  Max:{:.1f}%".format(
                    temp_actuelle, temp_max, hum_actuelle, hum_max))
            

    