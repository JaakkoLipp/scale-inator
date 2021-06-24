###########
### GUI ###
###########
import tkinter as tk, tkinter.font as tkFont, datetime, sys
from time import sleep
#from tkinter.ttk import *

def createWindow(x,collector,weight):
        #init tk
    window = tk.Tk()
    #window size, font
    window.geometry("800x480")
    fontStyle = tkFont.Font(family="Helvetica bold", size=20)

    #compile window
    if x==True:
        window.configure(bg='Green')
        text1="#",collector,"SUCCESSFULLY SAVED"
        label = tk.Label(text=text1, bg="White")

    if x==False:
        window.configure(bg='Red')
        label = tk.Label(text="SAME AS PREVIOUS,\nNOT ACCEPTED", bg="White")

    label.config(font=('Helvetica bold',28))
    label.pack()
    window.after(5000, lambda: window.destroy())
    window.mainloop()



createWindow(True,12,"4.20kg")
createWindow(False,0,0)
