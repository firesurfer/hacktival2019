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
    #parser.add_argument('subtitlefilename')
    args = parser.parse_args()
    url = Path(args.url)
    
    loader = SubscriptionDownloader(url)
    loader.download()
    while not loader.downloadFinished():
        sleep(1)
    
    #subpath = Path(args.subtitlefilename)
    #if not videopath.is_file() or not subpath.is_file():
    #    raise Exception

    window = MainWindow(loader)
    window.show()
    sys.exit(app.exec_())
