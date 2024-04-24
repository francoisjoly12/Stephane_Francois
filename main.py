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
#test

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

# Variables de temps
last_display_time = time.monotonic()
last_measurement_time = time.monotonic()
print_time = None

# Variables de température
temp_actuelle: float = bmp280.temperature
temp_moyenne: float = 0
temp_max: float = temp_actuelle
temp_min: float = temp_actuelle
historique_temperature = [temp_actuelle]
projet2.conversion_en_fahrenheit = False
projet2.resetMinMax = False

# Connexion à Adafruit,souscription aux feeds,collecte de l'heure et gestion de la connexion
io=None
not_connected=False
def connect_to_internet():
    io=None
    try:
        io = projet2.connecter_mqtt()
        if io.is_connected:
            io.subscribe("projet-2-Celcius/Farenheit")
            io.subscribe("projet-2-resetTime")
            ntp = adafruit_ntp.NTP(projet2.pool, tz_offset=-4)
            rtc.datetime = ntp.datetime     
        else:
            io=False
    except (ConnectionError):
        print("Pas de connexion internet")
    return io

io=connect_to_internet()
   
# Boucle principale
while True:
    if not io or io ==None :
        not_connected=True
    elif  not io.is_connected:
        not_connected=True
    
    current_time = time.monotonic()
    if current_time - last_measurement_time > 1:
        last_measurement_time = current_time
        last_connexion_time =current_time
        temp_max = max(temp_max, temp_actuelle)
        temp_min = min(temp_min, temp_actuelle)

        # Prise de température
        nouvelle_temp = bmp280.temperature
        temp_actuelle = nouvelle_temp
        
        # Calcul de la moyenne glissante
        historique_temperature.append(nouvelle_temp)
        historique_temperature = historique_temperature[-300:]  #Je refais mon tableau en prenant les 300 dernières entrées du tableau (5min)
        temp_moyenne = sum(historique_temperature) / len(historique_temperature)
    
        # Sauvegarde des données sur la carte SD et buffer
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
        if not_connected:       # Buffer de données
                    buffered_data = []
                    buffered_data.append([date, valeur])
  
    if not not_connected: # Connexion active à internet
        try:
            io.loop()
            # Reset du Min/Max 
            if projet2.resetMinMax:
                temp_min = temp_actuelle
                temp_max = temp_actuelle
                projet2.resetMinMax = False
            else:
                if temp_min == 0:  # Vérifier si temp_min a été réinitialisé
                    temp_min = temp_actuelle
                temp_max = max(temp_max, temp_actuelle)
                temp_min = min(temp_min, temp_actuelle)

            # publish feed
            try:
                io.publish_multiple([("projet-2-temps", temp_actuelle),("projet-2-tempsMoy", temp_moyenne),
                                     ("projet-2-tempsMin", temp_min),("projet-2-tempsMax", temp_max)],0)
            except (ValueError, RuntimeError, OSError) as e:
                print("Erreur lors de la publication des données")
                not_connected=True      # Active le buffer de données
        except (ValueError, RuntimeError, OSError) as e:
            print(e)
            not_connected=True      # Active le buffer de données
           
    elif not_connected: # Connexion perdue
        try:
            io=connect_to_internet()  # Tente de se reconnecter
            if io.is_connected:
                try:  
                    for data in buffered_data:
                        date_buf, value_buf =data
                        io.publish("projet-2-temps",value_buf, date_buf)
                    buffered_data.clear()  
                    not_connected=False                
                except Exception as e:
                    print("Erreur lors de la publication des données")
                    not_connected=True
        except Exception as e:
            print("Attente du rétablissement de la connexion")
            not_connected=True

    # Affichage sur écran
    if current_time - last_display_time > 0.5:
        last_display_time = current_time

        # Affichage en farenheit
        if projet2.conversion_en_fahrenheit:
            temp_actuelle_fahrenheit = projet2.celsius_to_fahrenheit(temp_actuelle)
            temp_moyenne_fahrenheit = projet2.celsius_to_fahrenheit(temp_moyenne)
            temp_min_fahrenheit = projet2.celsius_to_fahrenheit(temp_min)
            temp_max_fahrenheit = projet2.celsius_to_fahrenheit(temp_max)
            ecran.rafraichir_texte(
                "Température\nactuelle:{:.1f}F\nMoyenne:{:.1f}F\nMin:{:.1f}F  Max:{:.1f}F".format(
                    temp_actuelle_fahrenheit, temp_moyenne_fahrenheit, temp_min_fahrenheit,
                    temp_max_fahrenheit))
            
        #Affichage en Celcius
        else:
            ecran.rafraichir_texte(
                "Température\nactuelle:{:.1f}C\nMoyenne:{:.1f}C\nMin:{:.1f}C  Max:{:.1f}C".format(
                    temp_actuelle, temp_moyenne, temp_min, temp_max))
            
# Notes sur l'exécution de mon programme:
# Dans sa forme actuelle, lorsqu'on désactive la connexion internet pour la réactiver ensuite, il est impossible de se reconnecter
# à Adafruit malgré que la connexion internet se rétabli avec l'esp32.
# Je n'ai pas trouvé de solution à ce problème.
# J'ai testé le buffer et le renvoie des données de celui-ci en me déconnectant explicitement par io.disconnect().
# Avec cette commande, la reconnexion s'effectue et le buffer fonctionne adéquatement.
# J'ai inclus un printscreen de mon dashboard d'Adafruit dans les commits nommé Print_Dashboard_Adafruit.png.