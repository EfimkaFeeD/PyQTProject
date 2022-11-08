from yt_dlp import YoutubeDL
from time import sleep
from sys import stdout

url = ['https://www.youtube.com/watch?v=BmllggGO4pM']
with YoutubeDL() as ydl:
    ydl.download(url)




