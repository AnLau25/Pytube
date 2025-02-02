from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
import ctypes  # For changing the taskbar icon
import os



window = Tk()
window.title('YT Video Downloader')
window.geometry('500x460+430+180')
window.resizable(height=False, width=False)

# Create Canvas
canvas = Canvas(window, width=500, height=460, bg='white')
canvas.pack()

# Logo
logo = PhotoImage(file='plantboy.png')
logo = logo.subsample(3, 3)
canvas.create_image(250, 80, image=logo)

# Frame for input elements
frame = Frame(window, bg="white")
canvas.create_window(250, 300, window=frame)  # Center the frame on the canvas

# Styling
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', background='#FFFFFF', font=('OCR A Extended', 15))
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

# Widgets inside Frame (Keeps Alignment)
url_label = ttk.Label(frame, text='URL aquí:', style='TLabel')
url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

url_entry = ttk.Entry(frame, width=50, style='TEntry')
url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

res_label = ttk.Label(frame, text='Resolución:', style='TLabel')
res_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

video_res = ttk.Combobox(frame, width=10)
video_res.grid(row=1, column=1, padx=10, pady=5, sticky="w")

find_res_btn = ttk.Button(frame, text='Buscar', style='TButton')
find_res_btn.grid(row=2, column=0, padx=10, pady=5, sticky='w')

prgrs_label = ttk.Label(frame, text='', style='TLabel')
prgrs_label.grid(row=3, column=1, padx=10, pady=5, sticky='w')

prgrs_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=450, mode='determinate')
prgrs_bar.grid(row=4, columnspan=3, padx=10, pady=5, sticky='w')

down_btn = ttk.Button(frame, text='Descargar', style='TButton')
down_btn.grid(row=5, column=1, padx=10, pady=5, sticky='w')

window.mainloop()
