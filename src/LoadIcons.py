from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
import os


class IconLoader():
    def __init__(self):
        self.icons = {"euro":"icon/euro.png" , "dollar":"icon/dollar.png", "length" : "icon/index.png", "environment" : "icon/environment.png", "nasa": "icon/nasa.png", "social":"icon/social.png", "military":"icon/military.png" , "area": "icon/area.png", "soccer":"icon/soccer.png", "ruler": "icon/ruler.png", "revolutions_per_minute": "icon/rpm.png", "physics":"icon/physics.png", "ft": "private_icons/USA.png", "foot ** 2": "private_icons/USA.png", "foot ** 3": "private_icons/USA.png", "m":"private_icons/europe.png", "meter ** 2": "private_icons/europe.png", "meter ** 3": "private_icons/europe.png", "horsepower":"icon/hp.png", "liter":"private_icons/europe.png", "degree":"private_icons/degree.png", "kilowatt": "private_icons/europe.png", "millimeter":"icons/index.png", "foot * force_pound": "private_icons/USA.png", "meter * newton":"private_icons/europe.png", "mile / gallon": "private_icons/USA.png", "liter / kilometer":"private_icons/europe.png", "inch ** 2" : "private_icons/USA.png", "millimeter ** 2": "private_icons/europe.png", "millimeter":"private_icons/europe.png"}
    def listIcons(self):
        return self.icons.keys()
    def getIcon(self,name):
        
        if name in self.icons and os.path.isfile(self.icons[name]):
            pixmap = QPixmap.fromImage(QImage(self.icons[name]))
            return pixmap
        else:
            return QPixmap.fromImage(QImage(self.icons["physics"]))
