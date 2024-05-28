# -----------------------------------------------------------------------------
# Script : Control_App.py
# Auteur : François Joly, Stephane_Provost
# Description : Programme de simulation d'une chambre forte avec ventillation.
#               Application de controle via broker mosquitto
# Date : 2024/05/27
# -----------------------------------------------------------------------------

from tkinter import *
from tkinter import PhotoImage
import paho.mqtt.client as mqtt

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid(sticky=N+S+E+W)
        self.blinker_state = False
        self.blinker_running = False

        # Initialisation MQTT
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("192.168.0.150", 1883, 60)
        self.mqtt_client.loop_start()
        
        # Topics
        self.mqtt_topic_gas = 'gas'
        self.mqtt_topic_hum = 'hum'
        self.mqtt_topic_alarm = 'alarm'
        self.mqtt_topic_door = 'door'
        self.mqtt_topic_fan_speed = 'fan_speed'
        self.mqtt_topic_mode = 'app_mode'
        self.mqtt_topic_fan_mode = 'fan_mode'

        self.create_widgets()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # S'abonner aux topics
        client.subscribe(self.mqtt_topic_alarm)
        client.subscribe(self.mqtt_topic_door)
        client.subscribe(self.mqtt_topic_fan_mode)
        client.subscribe(self.mqtt_topic_fan_speed)
        client.subscribe(self.mqtt_topic_hum)
        client.subscribe(self.mqtt_topic_gas)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Message received on topic {topic}: {payload}")
        # Jauges
        if topic == self.mqtt_topic_hum:
            self.update_humidity_gauge(float(payload))
        elif topic == self.mqtt_topic_gas:
            self.update_gas_gauge(float(payload))
        elif topic == self.mqtt_topic_fan_speed:
            self.update_fan_speed_gauge(float(payload))
        # Label des boutons
        elif topic == self.mqtt_topic_alarm:
            self.update_alarm_display(str(payload))
        elif topic == self.mqtt_topic_door:
            self.update_door_display(payload)
        elif topic == self.mqtt_topic_fan_mode:
            self.update_fan_mode(str(payload))
            self.update_fan_on_off_display(str(payload))

    def create_widgets(self):
        self.canvas_width = 300
        self.canvas_height = 300
        self.on_image = PhotoImage(file="on.png")
        self.off_image = PhotoImage(file="off.png")

        self.cnvs_humidity = self.create_gauge("Humidity", 0, 0)
        self.cnvs_gas = self.create_gauge("Gas", 0, 1)
        self.cnvs_fan_speed = self.create_gauge("Fan Speed", 1, 0)
        
        self.id_needle_humidity, self.id_text_humidity = self.init_gauge(self.cnvs_humidity, "Humidity")
        self.id_needle_gas, self.id_text_gas = self.init_gauge(self.cnvs_gas, "Gas")
        self.id_needle_fan_speed, self.id_text_fan_speed = self.init_gauge(self.cnvs_fan_speed, "Fan Speed")
        self.id_text_fan_mode = self.cnvs_fan_speed.create_text(150, 250, font="Times 12 bold", text="Mode: Push")

        self.create_buttons()
        self.create_blinker()
        self.switch_mode(self.manual_button, self.manual_label)

    def create_gauge(self, title, row, column):
        cnvs = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        cnvs.grid(row=row, column=column, padx=5, pady=5)
        coord = 10, 50, 300, 300

        for i in range(8):
            cnvs.create_arc(coord, start=(i * (120 / 8) + 30), extent=(120 / 8), fill="white", width=1)
        cnvs.create_arc(coord, start=30, extent=120, outline="green", style="arc", width=30)
        cnvs.create_arc(coord, start=30, extent=20, outline="red", style="arc", width=30)
        cnvs.create_arc(coord, start=50, extent=20, outline="yellow", style="arc", width=30)
        cnvs.create_text(150, 15, font="Times 16 italic bold", text=title)
        cnvs.create_text(25, 140, font="Times 12 bold", text=0)
        cnvs.create_text(280, 140, font="Times 12 bold", text=100)
        return cnvs

    def init_gauge(self, cnvs, title):
        coord = 10, 50, 300, 300
        id_needle = cnvs.create_arc(coord, start=119, extent=1, width=7)
        id_text = cnvs.create_text(150, 210, font="Times 12 bold")
        return id_needle, id_text

    def create_buttons(self):
        self.frame_buttons = Frame(self)
        self.frame_buttons.grid(row=2, column=0, columnspan=2, sticky=W, padx=5, pady=5)

        self.manual_label = Label(self.frame_buttons, text="Mode : Auto", font=("Helvetica", 14), fg="green")
        self.manual_label.grid(row=0, column=8, columnspan=2, sticky=W, padx=20)
        self.manual_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch_mode(self.manual_button, self.manual_label), bd=0)
        self.manual_button.grid(row=1, column=8, columnspan=2, sticky=W, padx=20)

        self.alarm_label = Label(self.frame_buttons, text="Alarm: On", font=("Helvetica", 14), fg="green")
        self.alarm_label.grid(row=0, column=0, columnspan=2, sticky=W, padx=20)
        self.alarm_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch_alarm(self.alarm_button, self.alarm_label), bd=0)
        self.alarm_button.grid(row=1, column=0, columnspan=2, sticky=W, padx=20)

        self.door_label = Label(self.frame_buttons, text="Door: Open", font=("Helvetica", 14), fg="green")
        self.door_label.grid(row=0, column=2, columnspan=2, sticky=W, padx=10)
        self.door_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch_door(self.door_button, self.door_label), bd=0)
        self.door_button.grid(row=1, column=2, columnspan=2, sticky=W, padx=20)

        self.fan_label = Label(self.frame_buttons, text="Fan: On", font=("Helvetica", 14), fg="green")
        self.fan_label.grid(row=0, column=6, columnspan=2, sticky=W, padx=20)
        self.fan_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch_fan(self.fan_button, self.fan_label), bd=0)
        self.fan_button.grid(row=1, column=6, columnspan=2, sticky=W, padx=20)

        self.switch_mode(self.manual_button, self.manual_label)

    def update_humidity_gauge(self, value=0):
        self.update_gauge(self.cnvs_humidity, self.id_text_humidity, self.id_needle_humidity, value, " %")
       
    def update_gas_gauge(self, value=0):
        self.update_gauge(self.cnvs_gas, self.id_text_gas, self.id_needle_gas, round(value, 2), " ppm")

    def update_fan_speed_gauge(self, value):
        self.update_gauge(self.cnvs_fan_speed, self.id_text_fan_speed, self.id_needle_fan_speed, abs(int(value * 100)), " %")

    def update_gauge(self, cnvs, id_text, id_needle, value, unit):
        cnvs.itemconfig(id_text, text=str(value) + unit)
        angle = 120 * (100 - value) / 100 + 30
        cnvs.itemconfig(id_needle, start=angle)

    def switch_mode(self, button, label):
        if "Auto" in label.cget("text"):
            button.config(image=self.off_image)
            label.config(text="Mode : Manuel", fg="grey")
            self.alarm_button.config(state=NORMAL)
            self.door_button.config(state=NORMAL)
            self.fan_button.config(state=NORMAL)
            self.mqtt_client.publish(self.mqtt_topic_mode, "Manuel")
        else:
            button.config(image=self.on_image)
            label.config(text="Mode : Auto", fg="green")
            self.alarm_button.config(state=DISABLED)
            self.door_button.config(state=DISABLED)
            self.fan_button.config(state=DISABLED)
            self.mqtt_client.publish(self.mqtt_topic_mode, "Auto")

    def switch_door(self, button, label):
        if button["image"] == str(self.on_image):
            button.config(image=self.off_image)
            label.config(text="Door: Down", fg="green")
            self.mqtt_client.publish(self.mqtt_topic_door, "Down")
        else:
            button.config(image=self.on_image)
            label.config(text="Door: Up", fg="green")
            self.mqtt_client.publish(self.mqtt_topic_door, "Up")

    def switch_alarm(self, button, label):
        if button["image"] == str(self.on_image):
            button.config(image=self.off_image)
            label.config(text="Alarm: Off", fg="green")
            self.mqtt_client.publish(self.mqtt_topic_alarm, "Off")
        else:
            button.config(image=self.on_image)
            label.config(text="Alarm: On", fg="green")
            self.mqtt_client.publish(self.mqtt_topic_alarm, "On")

    def switch_fan(self, button, label):
        if button["image"] == str(self.on_image):
            button.config(image=self.off_image)
            label.config(text="Fan: Off", fg="green")
            self.mqtt_client.publish(self.mqtt_topic_fan_mode, "Off")
        else:
            button.config(image=self.on_image)
            label.config(text="Fan: On", fg="green")
            self.mqtt_client.publish(self.mqtt_topic_fan_mode, "On")

    def update_fan_mode(self, mode):
        self.cnvs_fan_speed.itemconfig(self.id_text_fan_mode, text=f"Mode: {mode}")

    def create_blinker(self):
        blinker_frame = Frame(self, bg='red')
        blinker_frame.grid(row=1, column=1, padx=5, pady=5, sticky=EW)
        self.blinker_canvas = Label(blinker_frame, text="ALARME", font=("Helvetica", 40, "bold"), fg="black", bg='red')
        self.blinker_canvas.pack(padx=10, pady=10)

    def flash_color(self):
        if self.blinker_state:
            current_color = self.blinker_canvas.cget("foreground")
            new_color = "black" if current_color == "white" else "white"
            self.blinker_canvas.config(foreground=new_color)
        if self.blinker_state:  
            self.after(500, self.flash_color)

    def update_alarm_display(self, state):
        if state == 'Alarme':
            self.blinker_state = True
            self.alarm_label.config(text="Alarm: On", fg="green")
            self.alarm_button.config(image=self.on_image) 
            if not self.blinker_running:
                self.blinker_running = True
                self.flash_color()
        elif state == "":
            self.blinker_state = False
            self.alarm_label.config(text="Alarm: Off", fg="green")
            self.alarm_button.config(image=self.off_image)  
            self.blinker_canvas.config(foreground='black')  
            self.blinker_running = False

    def update_door_display(self, state):
        self.door_label.config(text=f"Door: {state}")
        if state == "Up":
            self.door_button.config(image=self.on_image)
            self.door_label.config(text="Door: Up", fg="green")
        else:
            self.door_label.config(text="Door: Down", fg="green")
            self.door_button.config(image=self.off_image)

    def update_fan_on_off_display(self, state):
        if state == "Off":
            self.fan_label.config(text="Fan: Off", fg="green")
            self.fan_button.config(image=self.off_image)
        else:
            self.fan_label.config(text="Fan: On", fg="green")
            self.fan_button.config(image=self.on_image)

if __name__ == "__main__":
    root = Tk()
    root.title('Control_App')
    root.geometry("650x750")
    app = Application(root)
    app.mainloop()


# Références:
# https://funprojects.blog/2021/02/19/gauges-in-a-python-canvas/
# https://www.geeksforgeeks.org/on-off-toggle-button-switch-in-tkinter/