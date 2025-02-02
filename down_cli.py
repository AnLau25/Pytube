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
            showinfo(title='Search Complete', message='Elije de las resoluciones disponobles')
        except:
            showerror(title='Error', message='Error al buscar resoluciones!\n'\
                'Posibles razones\n->Conexion inestable\n->Link invalido')

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
