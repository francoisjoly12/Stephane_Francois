import os
import board
import digitalio
import analogio
import time
import adafruit_bmp280
import projet2
import adafruit_sdcard
import busio
import storage
import rtc
import json
import adafruit_datetime
import pcf8523
import adafruit_ntp

#parce que mon feed_callback ne fonctionne pas
#changer pour faren pour tester l'affichage en farenheit
#celcipour celcius
boutonToggle = "celci"
#meme chose pour boutonReset
#pousser un 1 pour mettre les valeur a 0
boutonReset = 0


# Mise en place des objets de la carte Arduino
i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1016.10
pot = analogio.AnalogIn(board.A0)

ecran = projet2.ecran()

temp_actuelleFinal = 0

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.IO15)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
rtc = pcf8523.PCF8523(i2c)


temp_actuelle: float = 0
temp_moyenne: float = 0
temp_max: float = -999
temp_min: float = 999
#une liste de temperature pour calculer la moyenne
list_temp = [0]

# récupère l'objet io depuis la fonction connecter_mqtt

io = projet2.connecter_mqtt()

ntp = adafruit_ntp.NTP(projet2.pool, tz_offset=-4)
rtc.datetime = ntp.datetime

last_time = time.monotonic()
last_time2 = time.monotonic()

#feed du bouton

io.subscribe("projet-2-bouton")
io.subscribe("projet-2-boutonReset")

while True:

    io.loop()
    #il me manque a avoirles info du feed(projet-2-bouton) pour le mettre dans la variable boutonToggle
    #je voit lefeed changer de state, mais je sais pas comment récuperer la variable
  
    #j'ai mis 2 car avec 1 je bust le data rate
    if(time.monotonic() - last_time > 2):
        
        temp_actuelle = bmp280.temperature

        if(boutonReset == "1"):
            print("Reset")
            
            temp_actuelle: float = 0
            temp_moyenne: float = 0
            temp_max: float = -999
            temp_min: float = 999
            for i in list_temp:
                list_temp[i] = temp_actuelleFinal

            boutonRest = 0

        if(boutonToggle == "faren"):
            #il y a une fonction dans projet2... mais ca marche comme ca aussi ! 
            temp_actuelleFinal = (temp_actuelle * 1.8) + 32

            if(temp_actuelleFinal > temp_max):
                temp_max = temp_actuelleFinal
            if(temp_actuelleFinal < temp_min):
                temp_min = temp_actuelleFinal        
        else:
            temp_actuelleFinal = temp_actuelle
            if(temp_actuelle > temp_max):
                temp_max = temp_actuelle
            if(temp_actuelle < temp_min):
                temp_min = temp_actuelle
        



        #pour que ma moyenne ne commence pas avec un valeur de 0 et prenne 5 min a avoir la bonne valeur
        if(list_temp[0] == 0):
            for i in list_temp:
                list_temp[i] = temp_actuelleFinal
        #ajoute la temperature lu a la liste de temperature pour effectuer la moyenne. puis delete la denriere valeur de la liste
        list_temp.append(temp_actuelleFinal)
        del list_temp[:-300]
        temp_moyenne = sum(list_temp)/len(list_temp)
        last_time = time.monotonic()

         #envoit les donné sur adafruit.io
        io.publish("projet-2-temp", temp_actuelle)
        io.publish("projet-2-tempMoy", temp_moyenne)



        
    

    #place l'heure de t = au temps du rtc qui est a jours
    t = rtc.datetime

    #format la date pour l'envoyé ensuite dans le dict data
    date = str("%d-%d-%d %d:%02d:%02d" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    data = {
        "date": date,
        "Value": temp_actuelle
        }

    #pousse les info dans le fichiers json
    with open("/sd/log.json", "a") as f:
        f.write(json.dumps(data))


    if (time.monotonic() - last_time2 > 0.5):
        if (boutonToggle == "faren"):
            ecran.rafraichir_texte("Température\nactuelle:{:.1f}C\nmoyenne:{:.1f}C\nmin:{:.1f}C  max:{:.1f}C".format(temp_actuelleFinal,temp_moyenne,temp_min,temp_max))
        else:
            ecran.rafraichir_texte("Température\nactuelle:{:.1f}C\nmoyenne:{:.1f}C\nmin:{:.1f}C  max:{:.1f}C".format(temp_actuelle,temp_moyenne,temp_min,temp_max))
