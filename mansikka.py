#illegal goods import
import openpyxl, tkinter as tk, tkinter.font as tkFont, serial, datetime

#serial port open

#GUI
window = tk.Tk()
#window size,colour,font
window.geometry("1280x720")
window.configure(bg='white')
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
#functional
label1 = tk.Label(text="Scale-inator")

#compile window
label1.pack()
line = tk.Entry()
line.pack()
window.mainloop()
