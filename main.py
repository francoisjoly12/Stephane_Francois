import board
import busio
import digitalio
import time
import adafruit_bmp280
import projet2
import json
import adafruit_sdcard
import busio
import storage
import pcf8523
from collections import OrderedDict
import adafruit_ntp
import rtc
import adafruit_dht

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
            

    