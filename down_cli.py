from pytube import YouTube

def searchResolution():
    vid_link = url_entry.get()
    if vid_link == '':
        showerror(title='Error', message='Pls incluya link del video')
    else:
        try:
            vid=YouTube(vid_link)
            rsltns=[]
            for i in video.streams.filter(file_extension='mp4'):
                rsltns.append(i.resolution)
            vid_rsltns['values']=rsltns
            showinfo(title='Busqueda Completada', message='Elije de las resoluciones disponobles')
        except:
            showerror(title='Error', message='Error al buscar resoluciones!\n'\
                'Posibles razones\n->Conexion inestable\n->Link invalido')

def download_vid():
    try:
        vid_link = url_entry.get()
        rsltn = video_res.get()
        if rsltn=='' and vid_link=='':
            showerror(title='Error', message='Faltan el link y la resolución')
        elif rsltn=='':
            showerror(title='Error', message='Seleccione una resolución')
        elif rsltn=='None':
            showerror(title='Error', message='La resolución no puede ser "Nada"')
        else:
            try:
                def on_progress(stream, chunks, bytes_left):
                    total_size= stream.filesize
                    
                    def get_form_size(total_size, factor=1024, suffix='B'):
                        for unit in ["","K","M","G","T","P","E","Z"]:
                            if total_size<factor:
                                return f"{tota_size:.2f}{unit}{suffix}"
                            tota_size/=factor
                    return f"{tota_size:.2f}Y{suffix}"
                formatted_size = get_form_size(total_size)
                            
            
        

# toma el URL del video como argumento
def vid_down(vid_url):
    vid = YouTube(vid_url)
    vid.streams.first().download()
    return vid.title

# toma input del usuario para el URL
try:
    vid_link = input('YT link here: ')
    print('Downloading video...')
    vid = vid_down(vid_link)
    print(f'"{vid}" downloaded')
except Exception as e:
    print(f'Failed to download video\nThe following might be the causes:\n-> No internet connection\n-> Invalid video link\n-> {e}')
