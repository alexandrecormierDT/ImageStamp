from pytube import YouTube
YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
print(video)

'''
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/test/code/pytybe.py

'''