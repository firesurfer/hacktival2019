from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
import os


class IconLoader():
    def __init__(self):
        self.icons = {"euro":"icon/euro.png" , "dollar":"icon/dollar.png", "length" : "icon/index.png", "environment" : "icon/environment.png", "nasa": "icon/nasa.png", "social":"icon/social.png", "military":"icon/military.png" , "area": "icon/area.png", "soccer":"icon/soccer.png", "ruler": "icon/ruler.png", "rpm": "icon/rpm.png", "physics":"icon/physics.png", "ft": "i"}
    def listIcons(self):
        return self.icons.keys()
    def getIcon(self,name):
        
        if name in self.icons and os.path.isfile(self.icons[name]):
            pixmap = QPixmap.fromImage(QImage(self.icons[name]))
            return pixmap
        else:
            return QPixmap.fromImage(QImage(self.icons["physics"]))
