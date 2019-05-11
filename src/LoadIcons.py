from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
import os


class IconLoader():
    def __init__(self):
        self.icons = {"euro":"icon/euro.png" , "dollar":"icon/dollar.png", "length" : "icon/index.png", "environment" : "icon/environment.png", "nasa": "icon/nasa.png", "social":"icon/social.png", "military":"icon/military.png" }
    def listIcons():
        return self.icons.keys()
    def getIcon(name):
        pixmap = QPixmap.fromImage(QImage(self.icons[name]))
        return pixmap
