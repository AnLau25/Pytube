from pytube import YouTube

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
