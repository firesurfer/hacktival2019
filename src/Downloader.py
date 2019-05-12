# Downloads the video and subtitles
from pathlib import Path
import os
import pickle

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import extractor

class SubscriptionDownloader:
    def __init__(self,url):
        self.url = str(url)
        self.video_id  = self.url[self.url.find("v=")+2:]
        self.dl_path = Path("./dl/" + self.video_id + "/")
        self.sub_path = self.dl_path / Path("sub.dmp")
        self.vid_path = self.dl_path / Path("vid.mp4")
        self.lastSub = {}
        self.title = ""
        self.offset = 0
        self.subtitleList = []
        if not Path.exists(self.dl_path):
            os.makedirs(self.dl_path)
    def download(self):
        print("Downloading...")
        try:
            self.title = YouTube(self.url).title
        except:
            pass
        if not Path.exists(self.vid_path):
            print("Downloading Video...")
            while True:
                try:
                    YouTube(self.url).streams.first().download(self.dl_path, "vid")
                    break
                except KeyError:
                    print("Download failed. Retry...")
        if not Path.exists(self.sub_path):
            print("Downloading Transcript...")
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
    def process(self):
        subtitleTemp = []
        for sub in self.subtitles:
            if type(sub) is dict:
                for key,value in sub.items():
                    for index,val in enumerate(value):
                        subtitleTemp.append(val)


       
        self.subtitleList = extractor.extract(subtitleTemp)
        
                        
    def subtitleAtPosition(self, secs):
       
        
        sub = self.subtitleList[0]
       
        start = float(sub["start"]) + self.offset
        end = float(sub["start"])+ float(sub["duration"])
        text = sub["text"]
        number = sub["values"]
        self.lastSub = sub
        for sub in self.subtitleList:
            
            start = float(sub["start"]) + self.offset
            end = float(sub["start"])+ float(sub["duration"])
            text = sub["text"]
            number = sub["values"]
                        
            if float(start) > float(secs):
               
                return self.lastSub

            self.lastSub = (start,end,text,number)
        return self.lastSub
    





