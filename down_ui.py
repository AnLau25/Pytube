from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
from PIL import Image, ImageTk
import os

# Function to fetch video resolutions
def find_resolution():
    vid_link = url_entry.get()
    if vid_link == '':
        showerror(title='Error', message='Por favor incluye el enlace del video')
    else:
        try:
            vid = YouTube(vid_link)
            resolutions = [stream.resolution for stream in vid.streams.filter(file_extension='mp4', res=True)]
            resolutions = list(set(resolutions))  # Remove duplicates
            resolutions.sort(reverse=True)  # Sort resolutions in descending order
            
            if not resolutions:
                showerror(title='Error', message='No se encontraron resoluciones disponibles')
                return
            
            resolutions['values'] = resolutions
            showinfo(title='Búsqueda Completada', message='Elige entre las resoluciones disponibles')
        except Exception as e:
            showerror(title='Error', message=f'Error al buscar resoluciones!\nRazones posibles:\n-> Conexión inestable\n-> Enlace inválido\n-> {e}')
            
#Runing searchResolution as a separate thread
def thread_findRes():
    t1 = threading.Thread(target=find_resolution)
    t1.start()
            
def thread_download():
    t2 = threading.Thread(target=download_vid)
    t2.start()
            
# Downloads the video
def download_vid():
    try:
        vid_link = url_entry.get().strip()
        rsltn = video_res.get()
        
        if not vid_link:
            showerror(title='Error', message='Falta el enlace del video')
            return
        if not rsltn:
            showerror(title='Error', message='Seleccione una resolución')
            return
        if rsltn == 'None':
            showerror(title='Error', message='La resolución no puede ser "Nada"')
            return
        
        down_btn.config(state="disabled")
        find_res_btn.config(state="disabled")
        window.update()
        
        def on_progress(stream, chunk, bytes_left):
            total_size = stream.filesize
            
            def get_form_size(size, factor=1024, suffix='B'):
                for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                    if size < factor:
                        return f"{size:.2f}{unit}{suffix}"
                    size /= factor
                return f"{size:.2f}Y{suffix}"
            
            formatted_size = get_form_size(total_size)
            bytes_downloaded = total_size - bytes_left
            percent_done = round(bytes_downloaded / total_size * 100)
            prgrs_bar['value'] = percent_done
            prgrs_label.config(text=f'{percent_done}%, Tamaño del archivo: {formatted_size}')
            window.update()
        
        vid = YouTube(vid_link, on_progress_callback=on_progress)
        stream = vid.streams.filter(res=rsltn, file_extension='mp4').first()
        
        down_btn.config(state="normal")
        find_res_btn.config(state="normal")
        
        if stream:
            stream.download()
            showinfo(title='Descarga Completa', message='El video ha sido descargado exitosamente.')
            prgrs_label.config(text='')
            prgrs_bar['value'] = 0
        else:
            showerror(title='Error de descarga', message='No se pudo descargar en esta resolución')
            prgrs_label.config(text='')
            prgrs_bar['value'] = 0
    except Exception as e:
        showerror(title='Error de descarga', message=f'Ha ocurrido un error al descargar el video.\nPosibles causas:\n-> Enlace no válido\n-> Falta de conexión\n-> {e}')
        prgrs_label.config(text='')
        prgrs_bar['value'] = 0

# Tkinter Window Setup
window = Tk()
window.title("YT Video Downloader")
window.geometry("500x460+430+180")
window.resizable(height=False, width=False)

# Create Canvas
canvas = Canvas(window, width=500, height=460, bg="white")
canvas.pack()

# Logo
logo_img = Image.open("plantboy.png")
logo_img = logo_img.resize((200, 150)) 
logo = ImageTk.PhotoImage(logo_img)
canvas.create_image(250, 80, image=logo)

# Frame for input elements
frame = Frame(window, bg="white")
canvas.create_window(250, 300, window=frame)

# Styling
label_style = ttk.Style()
label_style.configure("TLabel", foreground="#000000", background="#FFFFFF", font=("OCR A Extended", 15))
entry_style = ttk.Style()
entry_style.configure("TEntry", font=("Dotum", 15))
button_style = ttk.Style()
button_style.configure("TButton", foreground="#000000", font="DotumChe")

# Widgets inside Frame
url_label = ttk.Label(frame, text="URL aquí:", style="TLabel")
url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

url_entry = ttk.Entry(frame, width=50, style="TEntry")
url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

res_label = ttk.Label(frame, text="Resolución:", style="TLabel")
res_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

video_res = ttk.Combobox(frame, width=10)
video_res.grid(row=1, column=1, padx=10, pady=5, sticky="w")

find_res_btn = ttk.Button(frame, text="Buscar", style="TButton", command=thread_findRes)
find_res_btn.grid(row=2, column=0, padx=10, pady=5, sticky="w")

prgrs_label = ttk.Label(frame, text="", style="TLabel")
prgrs_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

prgrs_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=450, mode="determinate")
prgrs_bar.grid(row=4, columnspan=3, padx=10, pady=5, sticky="w")

down_btn = ttk.Button(frame, text="Descargar", style="TButton", command=thread_download)
down_btn.grid(row=5, column=1, padx=10, pady=5, sticky="w")

window.mainloop()
