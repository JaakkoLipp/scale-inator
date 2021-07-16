'''
###########
### GUI ###
###########
'''
try:
    from tkinter import font as tkFont
    import tkinter as tk
except ImportError:
    raise ImportError("TK couldn't be imported, make sure its installed")


def createWindow(x, collector, weight):
    # init tk
    window = tk.Tk()
    # window size, font
    window.geometry("800x240")
    fontStyle = tkFont.Font(family="Helvetica bold", size=48)  # noqa: F841

    # compile window
    if x:
        window.configure(bg='Green')
        text1 = ("#%s,\nSUCCESSFULLY SAVED\n %skg" % (collector, weight))
        label = tk.Label(text=text1, bg="Green", fg="white")

    if not x:
        window.configure(bg='Red')
        label = tk.Label(text="\nNOT ACCEPTED", bg="Red", fg="white")
    # configs
    label.config(font=('Helvetica bold', 48))
    label.pack()
    window.after(1500, lambda: window.destroy())
    window.mainloop()


"""test"""
# createWindow(True,12,4.20)
# createWindow(False,0,0)
