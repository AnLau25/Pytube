from tkinter import *
from tkinter import ttk
from pytubefix import YouTube
from pytubefix.cli import on_progress
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror
import threading
from PIL import Image, ImageTk
import subprocess
import os

#function to select the storage folder
def folder_select():
    global folder_dir
    folder_dir = filedialog.askdirectory()

# Function to fetch video resolutions
def find_resolution():
    vid_link = url_entry.get().strip()
    if vid_link == '':
        showerror(title='Error', message='Por favor incluye el enlace del video')
    else:
        try:
            vid = YouTube(vid_link)
            
            if video_type.get() == "Audio":
                audios = [f"{stream.abr}" for stream in vid.streams.filter(only_audio=True) if stream.abr]
                audios = list(set(audios))  # Remove duplicates
                audios.sort(reverse=True)
                
                if not audios:
                    showerror(title='Error', message='No se encontraron audios disponibles')
                    return
                
                video_res['values'] = audios
                
            else:
                videos = [stream.resolution for stream in vid.streams.filter(file_extension='mp4', res=True) if stream.resolution is not None]
                videos = list(set(videos))  # Remove duplicates
                videos.sort(reverse=True)  # Sort resolutions in descending order
                
                if not videos:
                    showerror(title='Error', message='No se encontraron resoluciones disponibles')
                    return
                
                video_res['values'] = videos
            
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
        
        def on_progress(stream, chunk, bytes_left):
            total_size = stream.filesize
            
            #def get_form_size(size, factor=1024, suffix='B'):
            #    for unit in ["", "K.p", "M", "G", "T", "P", "E", "Z"]:
            #        if size < factor:
            #            return f"{size:.2f}{unit}{suffix}"
            #        size /= factor
            #    return f"{size:.2f}Y{suffix}"
            
            #formatted_size = get_form_size(total_size)
            bytes_downloaded = total_size - bytes_left
            percent_done = round(bytes_downloaded / total_size * 100)
            prgrs_bar['value'] = percent_done
            prgrs_label.config(text=f'{percent_done}% completado')
            window.update()
        
        vid = YouTube(vid_link, on_progress_callback=on_progress)
        
        if video_type.get() == "Audio":
            stream = vid.streams.filter(only_audio=True, abr=rsltn).first()
            file_path = stream.download(output_path= folder_dir if folder_dir else None)
        
            base, ext = os.path.splitext(file_path)
            new_file = base + '.mp3'
            os.rename(file_path, new_file)
        else:
            stream = vid.streams.filter(progressive=True, res=rsltn, file_extension='mp4').first()

            if stream:
                stream.download(output_path=folder_dir if folder_dir else None)
            else:
                video_stream = vid.streams.filter(adaptive=True, res=rsltn, file_extension='mp4').first()
                #video_stream = vid.streams.filter(adaptive=True, res=rsltn, file_extension='mp4', only_video=True).first()
                #ffmpeg not recognized
                audio_stream = vid.streams.filter(adaptive=True, only_audio=True, file_extension='mp4').first()
                
                if not video_stream or not audio_stream:
                    showerror(title='Error', message='No se encontraron streams adecuados')
                    return
                video_path = video_stream.download(filename="video.mp4", output_path=folder_dir)
                audio_path = audio_stream.download(filename="audio.mp4", output_path=folder_dir)

                output_path = os.path.join(folder_dir, vid.title + ".mp4")

                # Use ffmpeg to merge
                command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{output_path}"'
                subprocess.call(command, shell=True)

                # Clean up temporary files
                os.remove(video_path)
                os.remove(audio_path)
                
        down_btn.config(state="normal")
        find_res_btn.config(state="normal")
                
        showinfo(title='Descarga Completa', message='El video ha sido descargado exitosamente.')
        prgrs_label.config(text='')
        prgrs_bar['value'] = 0
      
    except Exception as e:
        showerror(title='Error de descarga', message=f'Ha ocurrido un error al descargar el video.\nPosibles causas:\n-> Enlace no válido\n-> Falta de conexión\n-> {e}')
        prgrs_label.config(text='')
        prgrs_bar['value'] = 0


#def download():
#   vid = url_entry.get()
#    video = YouTube(vid)
#    video = video.streams.filter(file_extension='mp4').get_highest_resolution()
#    video.download()

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

url_entry = ttk.Entry(frame, width=40, style="TEntry")
url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

type_label = ttk.Label(frame, text="Tipo de video:", style="TLabel")
type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

video_type = ttk.Combobox(frame, values=["Video", "Audio"] ,width=10)
video_type.current(0)
video_type.grid(row=1, column=1, padx=10, pady=5, sticky="w")

res_label = ttk.Label(frame, text="Resolución:", style="TLabel")
res_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

video_res = ttk.Combobox(frame, width=10)
video_res.grid(row=2, column=1, padx=10, pady=5, sticky="w")

find_res_btn = ttk.Button(frame, text="Buscar", style="TButton", command=thread_findRes)
find_res_btn.grid(row=3, column=0, padx=10, pady=5, sticky="w")

prgrs_label = ttk.Label(frame, text="", style="TLabel")
prgrs_label.grid(row=4, columnspan=2, padx=10, pady=5, sticky="w")

prgrs_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=450, mode="determinate")
prgrs_bar.grid(row=5, columnspan=2, padx=10, pady=5, sticky="w")

fold_btn = down_btn = ttk.Button(frame, text="Fichero", style="TButton", command=folder_select)
fold_btn.grid(row=6, column=0, padx=10, pady=5, sticky="w")

down_btn = ttk.Button(frame, text="Descargar", style="TButton", command=thread_download)
down_btn.grid(row=6, column=1, padx=10, pady=5, sticky="w")

window.mainloop()
#working on joining video and sound
