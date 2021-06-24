###########
### GUI ###
###########
import tkinter as tk, tkinter.font as tkFont, datetime, sys
from tkinter.ttk import *

def createWindow():
        #init tk
    window = tk.Tk()
    #window size, colour, font
    window.geometry("480x480")
    window.configure(bg='white')
    fontStyle = tkFont.Font(family="Helvetica bold", size=20)
    label = tk.Label(text="test", bg="white")
    label.config(font=('Helvetica bold',28))

    input = tk.Entry(width=50)
    ###id = input.get()
    ###weight = "x"
    #compile window
    label.pack()
    input.pack()
    window.mainloop()

def setBgColour(x):
        #colours
    if x==True:
        window.configure(bg='Green')
    if x==False:
        window.configure(bg='Red')


createWindow()
