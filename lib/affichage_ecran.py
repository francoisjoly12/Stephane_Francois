import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import time

class Ecran:

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

    def refresh_text(self, humidity, gas_level, door_state, fan_state):
        self.text_area.text = "Hum: {:.1f}%\tGaz: {:.1f} ppm\nPorte: {}\tVent: {}\nMode: {}\nMQTT: {}".format(
                    humidity, gas_level, door_state, fan_state, mode,connection)
        self.display.refresh()


last_display_time = time.monotonic()
last_measurement_time = time.monotonic()
humidity = 0
gas_level = 0
door_state = "Up"
fan_state = "Push"
mode = "auto"
connection= "connecté"

ecran = Ecran()

while True:
    current_time = time.monotonic()
    if current_time - last_display_time > 0.5:
        last_display_time = current_time

    ecran.refresh_text(humidity, gas_level, door_state, fan_state)
