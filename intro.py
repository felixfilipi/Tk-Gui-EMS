import tkinter as tk
from tkinter import *
from tkinter import ttk
import login

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.setWindow()
    
    def setWindow(self):
        width = 300
        height = 100
        halfWidth = (self.parent.winfo_screenwidth() - width) // 2
        halfHeight = (self.parent.winfo_screenheight() - height) // 2

        # configure the window in the center of the screen
        self.parent.geometry("%ix%i+%i+%i" % (width, height, halfWidth, halfHeight))
        # configure image by label
        Label(self.parent, text = "Loading", bg = "#e88b64", fg = "white",
                font = ("Helvetica", 20), width = 9, height = 2).pack(
                        side = TOP, anchor = N, fill = X)
        s = ttk.Style()
        s.theme_use('alt')
        # configure horizontal progressbar
        s.configure("red.Horizontal.TProgressbar", background = 'red', 
                foreground = "red", relief = FLAT, bd = 0, height = 2)
        self.progress = ttk.Progressbar(self.parent, 
                style = "red.Horizontal.TProgressbar", orient = "horizontal", 
                length = 600, mode = "determinate")

        self.progress.pack(side = TOP, anchor = N, padx = 10)
        self.bytes = 0
        self.maxbytes = 0
        self.start()
    
    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()
        if self.progress["value"] == 60000:
            self.parent.destroy()
            if self.parent.destroy:
                login.main()

    def read_bytes(self):
        self.bytes += 1000
        self.progress['value'] = self.bytes
        self.progress.after(100, self.start)

def main():
    root = Tk()
    root.configure(bg = "#a86245")
    # remove title and window frame limit
    root.overrideredirect(True)
    SplashScreen(root)
    root.mainloop()

main()
