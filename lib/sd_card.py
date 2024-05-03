#sd_card.py
import board
import digitalio
import busio
import adafruit_sdcard
import storage
import rtc
import json
from collections import OrderedDict

class SDLogger:
    def __init__(self, sd_cs_pin):
        self.sd_detected = False
        self.sd_cs_pin = sd_cs_pin

    def initialize(self):
        try:
            spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
            cs = digitalio.DigitalInOut(self.sd_cs_pin)
            self.sd_card = adafruit_sdcard.SDCard(spi, cs)
            vfs = storage.VfsFat(self.sd_card)
            storage.mount(vfs, "/sd")
            self.sd_detected = True
            print("Carte SD détectée.")
        except Exception as e:
            print("Aucune carte SD détectée.")
    
    def log_data(self, data):
        if self.sd_detected:
            try:
                with open("/sd/log.json", "a") as file:
                    print_time = rtc.datetime
                    date = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(print_time.tm_year, print_time.tm_mon, print_time.tm_mday,
                                                                                 print_time.tm_hour, print_time.tm_min, print_time.tm_sec)
                    data["date"] = date
                    
                    file.write(json.dumps(data) + "\n")
                    
            except OSError as e:
                print("Erreur lors de l'écriture des données")
