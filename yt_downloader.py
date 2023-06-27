import os
import yt_dlp
import tempfile
from yt_dlp import YoutubeDL

def get_audio(urls):
    temp_dir = tempfile.gettempdir()

    ydl = yt_dlp.YoutubeDL({
        'quiet': True,
        'verbose': False,
        'format': 'bestaudio',
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        'postprocessors': [{'preferredcodec': 'mp3', 'preferredquality': '192', 'key': 'FFmpegExtractAudio', }],
    })

    paths = {}

    for url in urls:
        result = ydl.extract_info(url, download=True)
        print(
            f"Downloaded video \"{result['title']}\". Generating subtitles..."
        )
        paths[result["title"]] = os.path.join(temp_dir, f"{result['id']}.mp3")

    return paths


URLS = ['https://www.youtube.com/watch?v=nOPd0H_MOYc']
print(get_audio(URLS))
#with YoutubeDL() as ydl:
    #ydl.download(URLS)
#get_audio("https://youtu.be/puyCwRIQhZM")
#yt_dlp.YoutubeDL.download(sound_list)

