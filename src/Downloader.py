# Downloads the video and subtitles
from pathlib import Path
import os
import pickle

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


class SubscriptionDownloader:
    def __init__(self,url):
        self.url = str(url)
        self.video_id  = self.url[self.url.find("v=")+2:]
        self.dl_path = Path("./dl/" + self.video_id + "/")
        self.sub_path = self.dl_path / Path("sub.dmp")
        self.vid_path = self.dl_path / Path("vid.mp4")
        self.lastText = ""
        if not Path.exists(self.dl_path):
            os.makedirs(self.dl_path)
    def download(self):
        if not Path.exists(self.vid_path):
            YouTube(self.url).streams.first().download(self.dl_path, "vid")
        if not Path.exists(self.sub_path):
            sub = YouTubeTranscriptApi.get_transcripts([self.video_id], languages=['en'])
            pickle.dump(sub, open(self.sub_path, "wb"))
        self.subtitles = pickle.load(open(self.sub_path,"rb"))
    def downloadFinished(self):
        finished = Path.exists(self.dl_path) and Path.exists(self.sub_path) and Path.exists(self.vid_path)
        return finished
    def videoPath(self):
        return self.vid_path
    def subtitlePath(self):
        return self.sub_path
    def subtitleAtPosition(self, secs, window = True):
       
        
        
        for sub in self.subtitles:
            if type(sub) is dict:
                for key,value in sub.items():
                    for index,val in enumerate(value):
                        #print(secs)
                        start = float(val["start"])
                        end = float(val["start"])+ float(val["duration"])
                        
                       
                        
                        if  float(start) > float(secs):
                            text = ""
                            if window: 
                                if index > 0:
                                    prevVal = value[index-1]
                                    text += prevVal["text"] + " "
                            
                            text += val["text"] + " "
                            if window:
                                nextVal = value[index+1]
                                text += nextVal["text"] + " "
                            self.lastText = text
                            return text
        return self.lastText
    

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
