#!/usr/bin/python3
import sys
import argparse
from pathlib import Path


from PyQt5.QtWidgets import  QApplication
from MainWindow import MainWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Parse input parameters (video and subtitle file)
    parser = argparse.ArgumentParser(description='Understanding units and costs better')
    parser.add_argument('videofilename')
    parser.add_argument('subtitlefilename')
    args = parser.parse_args()
    videopath = Path(args.videofilename)
    subpath = Path(args.subtitlefilename)
    if not videopath.is_file() or not subpath.is_file():
        raise Exception

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
