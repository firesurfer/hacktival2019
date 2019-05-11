# Downloads the video and subtitles
from pathlib import Path
import os
import pickle

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


def get_vid_and_sub_path(url):
    video_id = url[url.find("v=")+2:]  # everything from the url from v= onwards
    dl_path = Path("../dl/" + video_id + "/")
    sub_path = dl_path / Path("sub.dmp")
    vid_path = dl_path / Path("vid.mp4")

    if not Path.exists(dl_path):
        os.makedirs(dl_path)
        YouTube(url).streams.first().download(dl_path, "vid")
        sub = YouTubeTranscriptApi.get_transcripts([video_id], languages=['en'])
        pickle.dump(sub, open(sub_path, "wb"))
        # To load:
        # sub = pickle.load(open(sub_path, "rb"))

    return sub_path, vid_path


if __name__ == "__main__":
    get_vid_and_sub_path("https://www.youtube.com/watch?v=RUVs_5mbJSA")
