from pytube import YouTube
import threading
from tkinter.messagebox import showerror, showinfo

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
            
            vid_rsltns['values'] = resolutions
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
        vid_link = url_entry.get()
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

# Descarga un video dado un URL
def vid_down(vid_url):
    try:
        vid = YouTube(vid_url)
        stream = vid.streams.get_highest_resolution()  # Selects the best available quality
        stream.download()
        return vid.title
    except Exception as e:
        print(f'Error al descargar el video: {e}')
        return None

# Toma input del usuario
try:
    vid_link = input('Ingrese el enlace de YouTube: ')
    print('Descargando video...')
    vid_title = vid_down(vid_link)
    if vid_title:
        print(f'Video "{vid_title}" descargado correctamente')
    else:
        print('No se pudo descargar el video.')
except Exception as e:
    print(f'Error general: {e}')

