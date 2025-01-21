from tkinter import*
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading

window= Tk()
window.title('YT video downloader')
window.geometry('500x460+430+180')
window.resizable(height=FALSE, width=FALSE)

canvas= Canvas(window, width=500, height=500)
canvas.config(bg='white')
canvas.pack()

logo= PhotoImage(file='plantboy.png')
logo= logo.subsample(3, 3)
canvas.create_image(250, 80, image=logo)

window.mainloop()