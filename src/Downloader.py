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
        self.title = ""
        self.offset = 0
        if not Path.exists(self.dl_path):
            os.makedirs(self.dl_path)
    def download(self):
        #self.title = YouTube(self.url).title
        if not Path.exists(self.vid_path):
            YouTube(self.url).streams.first().download(self.dl_path, "vid")
        if not Path.exists(self.sub_path):
            sub = YouTubeTranscriptApi.get_transcripts([self.video_id], languages=['en'])
            pickle.dump(sub, open(self.sub_path, "wb"))
        self.subtitles = pickle.load(open(self.sub_path,"rb"))
    def downloadFinished(self):
        finished = Path.exists(self.dl_path) and Path.exists(self.sub_path) and Path.exists(self.vid_path)
        return finished
    def videoTitle(self):
        return self.title
    def videoPath(self):
        return self.vid_path
    def subtitlePath(self):
        return self.sub_path
    def setOffset(self, off):
        self.offset = off
    def subtitleAtPosition(self, secs, window = True):
       
        
        
        for sub in self.subtitles:
            if type(sub) is dict:
                for key,value in sub.items():
                    for index,val in enumerate(value):
                        #print(secs)
                        start = float(val["start"]) + self.offset
                        end = float(val["start"])+ float(val["duration"])
                        
                       
                        
                        if  float(start) > float(secs):
                            text = ""
                            #If you need the step before comment in
                            #if window:  
                            #    if index > 0:
                            #        prevVal = value[index-1]
                            #        text += prevVal["text"] + " "
                            
                            text += val["text"] + " "
                            if window:
                                nextVal = value[index+1]
                                text += nextVal["text"] + " "
                            self.lastText = text
                            return text
        return self.lastText
    





