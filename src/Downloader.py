# Downloads the video and subtitles
from pathlib import Path
import os

from pytube import YouTube
import youtube_transcript_api

url = "https://www.youtube.com/watch?v=n06H7OcPd-g"

video_id = url[url.find("v=")+2:]  # everything from the url from v= onwards
print(video_id)
dl_path = Path("../dl/" + video_id + "/")
if not Path.exists(dl_path):
    os.makedirs(dl_path)
    YouTube(url).streams.first().download(dl_path)  # Source : https://stackoverflow.com/questions/40713268
else:
    pass  # Todo: check if video and subtitle file is there (?)



