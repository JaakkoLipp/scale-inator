###########
### GUI ###
###########
import tkinter as tk, tkinter.font as tkFont, datetime, sys

def createWindow():
    #init tk
    window = tk.Tk()
    #window size, colour, font
    window.geometry("1280x720")
    window.configure(bg='white')
    fontStyle = tkFont.Font(family="Helvetica bold", size=20)
    label = tk.Label(text="Vaakanaattori9000", bg="white")
    label.config(font=('Helvetica bold',28))

    input = tk.Entry(width=50)
    ###id = input.get()
    ###weight = "x"
    #compile window
    label.pack()
    input.pack()

    window.mainloop()
