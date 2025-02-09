from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
import os


# Function to fetch video resolutions
def fetch_resolutions():
    url = url_entry.get()
    if not url:
        showerror("Error", "Por favor, ingrese un URL válido.")
        return

    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        resolutions = sorted(set(stream.resolution for stream in streams if stream.resolution), reverse=True)
        video_res["values"] = resolutions
        if resolutions:
            video_res.current(0)  # Set first resolution as default
        else:
            showerror("Error", "No se encontraron resoluciones disponibles.")
    except Exception as e:
        showerror("Error", f"No se pudo obtener resoluciones.\n{str(e)}")


# Function to update progress bar
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    downloaded = total_size - bytes_remaining
    percentage = (downloaded / total_size) * 100
    prgrs_bar["value"] = percentage
    prgrs_label["text"] = f"Descargando... {int(percentage)}%"


# Function to download video
def download_video():
    url = url_entry.get()
    resolution = video_res.get()

    if not url or not resolution:
        showerror("Error", "Por favor, ingrese un URL válido y seleccione una resolución.")
        return

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution, file_extension="mp4").first()
        
        if not stream:
            showerror("Error", "No se encontró la resolución seleccionada.")
            return

        save_path = os.path.expanduser("~/Downloads")
        prgrs_label["text"] = "Descargando..."
        stream.download(save_path)
        showinfo("Completado", f"Descarga completada. Archivo guardado en:\n{save_path}")
        prgrs_label["text"] = "Descarga completada"
        prgrs_bar["value"] = 0  # Reset progress bar

    except Exception as e:
        showerror("Error", f"No se pudo descargar el video.\n{str(e)}")


# Function to run download in separate thread
def start_download():
    threading.Thread(target=download_video, daemon=True).start()


# Tkinter Window Setup
window = Tk()
window.title("YT Video Downloader")
window.geometry("500x460+430+180")
window.resizable(height=False, width=False)

# Create Canvas
canvas = Canvas(window, width=500, height=460, bg="white")
canvas.pack()

# Logo
logo = PhotoImage(file="plantboy.png")
logo = logo.subsample(3, 3)
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

find_res_btn = ttk.Button(frame, text="Buscar", style="TButton", command=fetch_resolutions)
find_res_btn.grid(row=2, column=0, padx=10, pady=5, sticky="w")

prgrs_label = ttk.Label(frame, text="", style="TLabel")
prgrs_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

prgrs_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=450, mode="determinate")
prgrs_bar.grid(row=4, columnspan=3, padx=10, pady=5, sticky="w")

down_btn = ttk.Button(frame, text="Descargar", style="TButton", command=start_download)
down_btn.grid(row=5, column=1, padx=10, pady=5, sticky="w")

window.mainloop()
