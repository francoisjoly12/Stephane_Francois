#Tkinter.py
from tkinter import * 
#from gaz_sensor import gas_value
#gas_value1 = gaz_sensor.gas_value
gas_value1 = 40000

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        self.label1 = Label(self, text="Humidité")
        self.label2 = Label(self, text="Gaz")
        self.label3 = Label(self, text="Capteur d'Obstacle")
        self.label4 = Label(self, text="Capteur laser")
        self.label5 = Label(self, text="État de la porte")
        self.label6 = Label(self, text="Ventilateur")

        self.label1.grid (row=0, column=0, sticky=W, columnspan=1)
        self.label2.grid (row=1, column=0, sticky=W, columnspan=1)
        self.label3.grid (row=2, column=0, sticky=W, columnspan=1)
        self.label4.grid (row=3, column=0, sticky=W, columnspan=1)
        self.label5.grid (row=4, column=0, sticky=W, columnspan=1)
        self.label6.grid (row=5, column=0, sticky=W, columnspan=1)

        self.number1 = Entry (self)
        self.number2 = Entry (self)
        self.number3 = Entry (self)
        self.number4 = Entry (self)
        self.number5 = Entry (self)
        self.number6 = Entry (self)

        self.number1.grid(row=0, column=1, sticky=W, columnspan=2)
        self.number2.grid(row=1, column=1, sticky=W, columnspan=2)
        self.number3.grid(row=2, column=1, sticky=W, columnspan=2)
        self.number4.grid(row=3, column=1, sticky=W, columnspan=2)
        self.number5.grid(row=4, column=1, sticky=W, columnspan=2)
        self.number6.grid(row=5, column=1, sticky=W, columnspan=2)

        self.button1 = Button(self,text='Manuel')#, command=self.Manuel)
        self.button1.grid(row =0, column = 3, sticky=W, columnspan=1)
        self.button2 = Button(self,text='Auto')#, command=self.Auto)
        self.button2.grid(row =0, column = 4, sticky=W, columnspan=1)

        gas_value = gas_value1
        self.number2.delete(0, END)
        self.number2.insert(0, gas_value1)
        
root = Tk()
root.title('Interface')
root.geometry('400x600')
app = Application(root)
app.mainloop()


