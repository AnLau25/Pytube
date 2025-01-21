from tkinter import*
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading

window= Tk()
window.title('YT video downloader')
window.geometry('500x460+430+180')
window.rezisable(height=FALSE, width=FALSE)
window.mainloop()

canvas= Canvas(window, width=500, height=400)
canvas.pack()