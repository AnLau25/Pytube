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

label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', background='#FFFFFF', font=('OCR A Extended', 15))
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum',15))
button_style = ttk.Style()
button_style.configure('TButton', foreground='#f4f4f4', font='DotumChe')

url_label = ttk.Label(window, text='URL aquí: ', style='TLabel')
url_entry = ttk.Entry(window, width=76, style='TEntry')
canvas.create_window(114, 200, window=url_label)
canvas.create_window(250, 230, window=url_entry)

window.mainloop()