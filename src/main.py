#!/usr/bin/python3
import sys
import argparse
from pathlib import Path


from PyQt5.QtWidgets import  QApplication
from MainWindow import MainWindow
import qdarkstyle
from Downloader import SubscriptionDownloader

if __name__ == "__main__":
    
    
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # Parse input parameters (video and subtitle file)
    parser = argparse.ArgumentParser(description='Understanding units and costs better')
    parser.add_argument('url')
    parser.add_argument("-o",'--offset', dest='offset', action='store', default=0, help='Pass an offset to the subtitle loader')
    parser.add_argument("-m",'--mute', dest='mute', action='store_true', default=False, help='Mute video')
    parser.add_argument("-s",'--subtitles', dest='subtitles', action='store_true', default=False, help='Show subtitles text')

    #parser.add_argument('subtitlefilename')
    args = parser.parse_args()
    url = Path(args.url)
    offset = float(args.offset)
    mute = args.mute
    subtitles = args.subtitles
    
    
    
    

    
    #subpath = Path(args.subtitlefilename)
    #if not videopath.is_file() or not subpath.is_file():
    #    raise Exception



    window = MainWindow(args)
    if mute:
        window.mute()
    if subtitles:
        window.enableSubtitles()
    window.show()
    sys.exit(app.exec_())
