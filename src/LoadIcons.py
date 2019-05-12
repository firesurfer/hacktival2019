from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
import os


class IconLoader():
    def __init__(self):
        self.icons = {"euro":"icon/euro.png" , "dollar":"icon/dollar.png", "length" : "icon/index.png", "environment" : "icon/environment.png", "nasa": "icon/nasa.png", "social":"icon/social.png", "military":"icon/military.png" , "area": "icon/area.png", "soccer":"icon/soccer.png", "ruler": "icon/ruler.png", "rpm": "icon/rpm.png", "physics":"icon/physics.png", "ft": "private_icons/ft.png", "foot ** 2": "private_icons/ft2.png", "foot ** 3": "private_icons/ft3.png", "m":"m.png", "m2": "m2.png", "m3": "m3.png", "hp":"icons/hp.png", "l":"private_icons/L.png", "°":"private_icons/dregree.png", "kW": "private_icons/kw.png"}
    def listIcons(self):
        return self.icons.keys()
    def getIcon(self,name):
        
        if name in self.icons and os.path.isfile(self.icons[name]):
            pixmap = QPixmap.fromImage(QImage(self.icons[name]))
            return pixmap
        else:
            return QPixmap.fromImage(QImage(self.icons["physics"]))
