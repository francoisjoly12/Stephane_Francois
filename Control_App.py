from tkinter import *
import random

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid(sticky=N+S+E+W)
        self.create_widgets()
        self.update_humidity_gauge()
        self.update_gas_gauge()
        self.update_fan_speed_gauge()

    def create_widgets(self):
        self.canvas_width = 300
        self.canvas_height = 300
        self.create_humidity_gauge()
        self.create_gas_gauge()
        self.create_fan_speed_gauge()
        self.on_image = PhotoImage(file="on.png")
        self.off_image = PhotoImage(file="off.png")
        self.create_buttons()

    def create_humidity_gauge(self):
        self.cnvs_humidity = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.cnvs_humidity.grid(row=0, column=0, padx=5, pady=5)
        coord = 10, 50, 300, 300

        for i in range(8):
            self.cnvs_humidity.create_arc(coord, start=(i * (120 / 8) + 30), extent=(120 / 8), fill="white", width=1)
        self.cnvs_humidity.create_arc(coord, start=30, extent=120, outline="green", style="arc", width=30)
        self.cnvs_humidity.create_arc(coord, start=30, extent=20, outline="red", style="arc", width=30)
        self.cnvs_humidity.create_arc(coord, start=50, extent=20, outline="yellow", style="arc", width=30)
        self.id_needle_humidity = self.cnvs_humidity.create_arc(coord, start=119, extent=1, width=7)
        self.cnvs_humidity.create_text(150, 15, font="Times 16 italic bold", text="Humidity")
        self.cnvs_humidity.create_text(25, 140, font="Times 12 bold", text=0)
        self.cnvs_humidity.create_text(280, 140, font="Times 12 bold", text=100)
        self.id_text_humidity = self.cnvs_humidity.create_text(150, 210, font="Times 12 bold")

    def create_gas_gauge(self):
        self.cnvs_gas = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.cnvs_gas.grid(row=0, column=1, padx=5, pady=5)
        coord = 10, 50, 300, 300

        for i in range(8):
            self.cnvs_gas.create_arc(coord, start=(i * (120 / 8) + 30), extent=(120 / 8), fill="white", width=1)
        self.cnvs_gas.create_arc(coord, start=30, extent=120, outline="green", style="arc", width=30)
        self.cnvs_gas.create_arc(coord, start=30, extent=20, outline="red", style="arc", width=30)
        self.cnvs_gas.create_arc(coord, start=50, extent=20, outline="yellow", style="arc", width=30)
        self.id_needle_gas = self.cnvs_gas.create_arc(coord, start=119, extent=1, width=7)
        self.cnvs_gas.create_text(150, 15, font="Times 16 italic bold", text="Gas")
        self.cnvs_gas.create_text(25, 140, font="Times 12 bold", text=0)
        self.cnvs_gas.create_text(280, 140, font="Times 12 bold", text=100)
        self.id_text_gas = self.cnvs_gas.create_text(150, 210, font="Times 12 bold")

    def create_fan_speed_gauge(self):
        self.cnvs_fan_speed = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.cnvs_fan_speed.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        coord = 10, 50, 300, 300

        for i in range(8):
            self.cnvs_fan_speed.create_arc(coord, start=(i * (120 / 8) + 30), extent=(120 / 8), fill="white", width=1)
        self.cnvs_fan_speed.create_arc(coord, start=30, extent=120, outline="green", style="arc", width=30)
        self.cnvs_fan_speed.create_arc(coord, start=30, extent=20, outline="red", style="arc", width=30)
        self.cnvs_fan_speed.create_arc(coord, start=50, extent=20, outline="yellow", style="arc", width=30)
        self.id_needle_fan_speed = self.cnvs_fan_speed.create_arc(coord, start=119, extent=1, width=7)
        self.cnvs_fan_speed.create_text(150, 15, font="Times 16 italic bold", text="Fan Speed")
        self.cnvs_fan_speed.create_text(25, 140, font="Times 12 bold", text=0)
        self.cnvs_fan_speed.create_text(280, 140, font="Times 12 bold", text=100)
        self.id_text_fan_speed = self.cnvs_fan_speed.create_text(150, 210, font="Times 12 bold")
        self.id_text_fan_mode = self.cnvs_fan_speed.create_text(150, 250, font="Times 12 bold", text="Mode: Push")

    def create_buttons(self):
        self.frame_buttons = Frame(self)
        self.frame_buttons.grid(row=2, column=0, columnspan=2, sticky=W, padx=5, pady=5)

        self.manual_label = Label(self.frame_buttons, text="Mode : Auto", font=("Helvetica", 14), fg="green")
        self.manual_label.grid(row=0, column=8, columnspan=2, sticky=W, pady=5)
        self.manual_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch_mode(self.manual_button, self.manual_label), bd=0)
        self.manual_button.grid(row=1, column=8, columnspan=2, sticky=W, pady=5)

        self.alarm_label = Label(self.frame_buttons, text="Alarm: On", font=("Helvetica", 14), fg="green")
        self.alarm_label.grid(row=0, column=0, columnspan=2, sticky=W, pady=5)
        self.alarm_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch(self.alarm_button, self.alarm_label), bd=0)
        self.alarm_button.grid(row=1, column=0, columnspan=2, sticky=W, pady=5)

        self.door_label = Label(self.frame_buttons, text="Door: On", font=("Helvetica", 14), fg="green")
        self.door_label.grid(row=0, column=2, columnspan=2, sticky=W, pady=5)
        self.door_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch(self.door_button, self.door_label), bd=0)
        self.door_button.grid(row=1, column=2, columnspan=2, sticky=W, pady=5)

        self.fan_label = Label(self.frame_buttons, text="Fan: On", font=("Helvetica", 14), fg="green")
        self.fan_label.grid(row=0, column=6, columnspan=2, sticky=W, pady=5)
        self.fan_button = Button(self.frame_buttons, image=self.on_image, command=lambda: self.switch(self.fan_button, self.fan_label), bd=0)
        self.fan_button.grid(row=1, column=6, columnspan=2, sticky=W, pady=5)

        self.switch_mode(self.manual_button, self.manual_label)

    def update_humidity_gauge(self):
        newvalue = random.randint(0, 100)
        self.cnvs_humidity.itemconfig(self.id_text_humidity, text=str(newvalue) + " %")
        angle = 120 * (100 - newvalue) / 100 + 30
        self.cnvs_humidity.itemconfig(self.id_needle_humidity, start=angle)
        self.after(3000, self.update_humidity_gauge)

    def update_gas_gauge(self):
        newvalue = random.randint(0, 100)
        self.cnvs_gas.itemconfig(self.id_text_gas, text=str(newvalue) + " ppm")
        angle = 120 * (100 - newvalue) / 100 + 30
        self.cnvs_gas.itemconfig(self.id_needle_gas, start=angle)
        self.after(3000, self.update_gas_gauge)

    def update_fan_speed_gauge(self):
        newvalue = random.randint(0, 100)
        self.cnvs_fan_speed.itemconfig(self.id_text_fan_speed, text=str(newvalue) + " RPM")
        angle = 120 * (100 - newvalue) / 100 + 30
        self.cnvs_fan_speed.itemconfig(self.id_needle_fan_speed, start=angle)
        self.after(3000, self.update_fan_speed_gauge)

    def switch_mode(self, button, label):
        if "Auto" in label.cget("text"):
            button.config(image=self.off_image)
            label.config(text="Mode : Manuel", fg="grey")
            self.alarm_button.config(state=NORMAL)
            self.door_button.config(state=NORMAL)
            self.fan_button.config(state=NORMAL)
        else:
            button.config(image=self.on_image)
            label.config(text="Mode : Auto", fg="green")
            self.alarm_button.config(state=DISABLED)
            self.door_button.config(state=DISABLED)
            self.fan_button.config(state=DISABLED)

    def switch(self, button, label):
        if button["image"] == str(self.on_image):
            button.config(image=self.off_image)
            label.config(text=label.cget("text").split(':')[0] + ": Off", fg="grey")
        else:
            button.config(image=self.on_image)
            label.config(text=label.cget("text").split(':')[0] + ": On", fg="green")

    def update_fan_mode(self, mode):
        if mode.lower() == 'push':
            self.cnvs_fan_speed.itemconfig(self.id_text_fan_mode, text="Mode: Push")
        else:
            self.cnvs_fan_speed.itemconfig(self.id_text_fan_mode, text="Mode: Pull")

if __name__ == "__main__":
    root = Tk()
    root.title('Control_App')
    root.geometry("650x750")
    app = Application(root)
    app.mainloop()