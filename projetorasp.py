from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter.ttk import Progressbar
from gpiozero import DistanceSensor
from time import sleep
from pyo import *
import alsaaudio

s = Server(duplex=1,audio="jack").boot()
s.start()
sensorFreq = DistanceSensor(echo=17,trigger=4)
sensorVol = DistanceSensor(echo=10,trigger=9)
high = 20
highestNote=1800


class Aplicacao:
   
    iniciar=False
    formatos={}
    formatoAtual="senoidal"
    def __init__(self, master=None):
        self.widget = Frame(master)
        self.widget.grid()
       
        self.msg = tk.Label(self.widget,text="Theremin muito louco",font=("Arial", 14))
        self.msg.grid(row=0,column=0,columnspan=3, pady=5)
        self.btn=tk.Button(self.widget,text='Iniciar',font="Arial 12",command=self.setIniciar, width=14,height=2)
        self.btn.grid(row=1,column=0,columnspan=3, pady=5)

       
        self.photo = tk.PhotoImage(file = "./senoidal.png")
        self.fotoSenoidal=self.photo.subsample(2, 2)
        self.formatos["senoidal"]=tk.Button(self.widget, image = self.fotoSenoidal, command= lambda: self.setFormato("senoidal"))
        self.formatos["senoidal"].grid(row=2, column=0,padx=3, pady=5)
       
        self.photo = tk.PhotoImage(file = "./quadrado.png")
        self.fotoQuadrado=self.photo.subsample(2, 2)
        self.formatos["quadrado"]=tk.Button(self.widget, image = self.fotoQuadrado, command= lambda: self.setFormato("quadrado"))
        self.formatos["quadrado"].grid(row=2, column=1,padx=3, pady=5)

        self.photo = tk.PhotoImage(file = "./dente.png")
        self.fotoDente=self.photo.subsample(2, 2)
        self.formatos["dente"]=tk.Button(self.widget, image = self.fotoDente, command= lambda: self.setFormato("dente"))
        self.formatos["dente"].grid(row=2, column=2,padx=3, pady=5)
 
       
        self.freqtxt = tk.Label(self.widget,text="leitura da frequência", font=("Arial", 12))
        self.freqtxt.grid(row=3,columnspan=3,padx=5, pady=5)
       
        self.freqRead = tk.Label(self.widget,text="", font=("Arial", 14))
        self.freqRead.grid(row=4,columnspan=3,padx=5, pady=5)
       
        tk.Label(self.widget,text="leitura do volume", font=("Arial", 12)).grid(row=5,columnspan=3,padx=5, pady=5)
       
        self.volProg = Progressbar(self.widget, orient=HORIZONTAL, length=200, mode='determinate')
        self.volProg.grid(row=6,columnspan=3,padx=5, pady=5)
       
        self.formatos[self.formatoAtual]['relief']=SUNKEN


       
    def setIniciar(self):
        self.iniciar = not self.iniciar
        if(self.iniciar):
            self.loop()
            self.btn['text']='Parar'
        else:
            self.btn['text']='Iniciar'
       

    def setFormato(self, formato):
        self.formatos[self.formatoAtual]['relief']=RAISED
        self.formatoAtual=formato
        print(self.formatoAtual)
        self.formatos[formato]['relief']=SUNKEN
       
    def getFormato(self):
        readVol = 100 - int(sensorVol.distance * 100)
        m = alsaaudio.Mixer('HDMI')
        current_volume = m.getvolume()
        m.setvolume(readVol)
        self.volProg['value']=readVol
        if(self.formatoAtual=="senoidal"):
            read = sensorFreq.distance * highestNote
            print(read)
            a = Sine(mul=5, freq=read).out()
            self.freqRead['text'] = int(read)
            sleep(0.1)
           
        elif(self.formatoAtual=="quadrada"):
            read = sensorFreq.distance * highestNote
            print(read)
            freq = [read * i for i in range(1,high) if i%2 == 1]
            harm = [0.33 / i for i in range(1,high) if i%2 == 1]
            a = Sine(mul=harm,freq=read).out()
            self.freqRead['text'] = int(read)
            sleep(0.1)

        else:
            read = sensorFreq.distance * highestNote
            print(read)
            a = SuperSaw(mul=5, freq=read).out()
            self.freqRead['text'] = int(read)
            sleep(0.1)
           
       
       
    def loop(self):
        if(self.iniciar):
            self.getFormato()
            root.after(50, lambda: self.loop())


       
root = tk.Tk()
interface = Aplicacao(root)
root.mainloop()
