import storage
import pcf8523
import board
import busio
import digitalio
import time
import adafruit_bmp280
import projet2
import json
import adafruit_sdcard



# Mise en place des objets de la carte Arduino
i2c = board.I2C()
rtc = pcf8523.PCF8523(i2c)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1016.10
led = digitalio.DigitalInOut(board.IO11)
led.direction = digitalio.Direction.OUTPUT
ecran = projet2.ecran()

# Initialisation de la carte SD
try:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.IO15)  
    sd_card = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sd_card)
    storage.mount(vfs, "/sd")
    sd_detected = True
except Exception as e:  # Ignore l'absence de carte SD
    sd_detected = False
if sd_detected:
    print("Carte SD détectée.")
else:
    print("Aucune carte SD détectée.")


if sd_detected:
            try:
                with open("/sd/log.json", "a") as file:
                    print_time = rtc.datetime
                    date=  "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(print_time.tm_year, print_time.tm_mon, print_time.tm_mday,
                                                                            print_time.tm_hour, print_time.tm_min, print_time.tm_sec)
                    valeur = "{:.1f}".format(temp_actuelle)
                    data= OrderedDict() #Pour changer l'ordre d'écriture des clés date et valeur
                    data["date"]=date
                    data["valeur"]=valeur
                    led.value = True  # turn on LED quand écrit
                    file.write(json.dumps(data) + "\n")
                    led.value = False  # turn off LED 
                file.close()  
            except OSError as e:
                print("Erreur lors de l'écritude des données")
  