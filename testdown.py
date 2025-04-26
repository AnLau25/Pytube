from pytube import YouTube

def download(link):
    video = YouTube(link)
    video = video.streams.filter(file_extentsion='mp4').get_highest_resolution()
    video.download()
    