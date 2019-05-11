from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
import os


class IconLoader():
    def __init__(self):
        self.icons = {"euro":"icon/euro.png" , "dollar":"icon/dollar.png", "length" : "icon/index.png", "environment" : "icon/environment.png", "nasa": "icon/nasa.png", "social":"icon/social.png", "military":"icon/military.png" , "area": "icon/area.png", "soccer":"icon/soccer.png", "ruler": "icon/ruler.png"}
    def listIcons(self):
        return self.icons.keys()
    def getIcon(self,name):
        if os.path.isfile(self.icons[name]):
            pixmap = QPixmap.fromImage(QImage(self.icons[name]))
            return pixmap
        else:
            return QPixmap(40,40)
