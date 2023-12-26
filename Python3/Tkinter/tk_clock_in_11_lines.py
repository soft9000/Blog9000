from tkinter import *
import time


zProgram = Tk()
zProgram.title("zClock: Python3 Clock in 11 Statements")
zClock = Label(zProgram,
               font=('ariel', 72, 'bold'),
               bg='gold',
               fg='white')
zClock.pack(fill=BOTH, expand=1)


def zTimer():
    zClock.config(text=time.strftime('%H:%M:%S'))
    zClock.after(500, zTimer)


zTimer()
zProgram.mainloop()


