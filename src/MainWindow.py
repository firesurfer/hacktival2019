from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QStyle, QWidget, QGraphicsTextItem, QGraphicsView, QGraphicsScene, QSpacerItem, QListWidget, QListWidgetItem
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtCore import  QDir, Qt, QUrl, QSizeF, QRectF, QPointF, QSize
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon  
import os
from Downloader import SubscriptionDownloader
from LoadIcons import IconLoader


class MainWindow(QMainWindow):

    #The subtitlePath is optional, if it is none we can run a speech recognition instead.
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
    
        self.initUI()

    def initUI(self):
       
        self.resize(1500,800)
        
        self.setWindowTitle("How Much Is That?         " + self.loader.videoTitle())
        centralWidget = MainWidget(self.loader)
        self.setCentralWidget(centralWidget)

        centralWidget.openVideo(os.path.abspath(self.loader.videoPath()))
       
       
       
        
class MainWidget(QWidget):
    resized = QtCore.pyqtSignal()
    def __init__(self,loader, parent=None):
        super().__init__(parent)
        self.loader = loader
        self.iconLoader = IconLoader()
        self.initUI()

    def getIconLoader(self):
        return self.iconLoader
    def openVideo(self,path):
        print(path)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(str(path))))

        
     
    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.notificationList = QListWidget()
        self.notificationList.setMinimumWidth(350)
        self.notificationList.setMaximumWidth(400)
        self.notificationList.setIconSize(QSize(45,45))
        self.playerLayout = QVBoxLayout()
        
       
        item = QListWidgetItem()
        item.setIcon(QIcon(self.iconLoader.getIcon("environment")))
        item.setText("Test")
        item.setFont(QFont("Arial",20))
        self.notificationList.addItem(item)
        
        self.mainLayout.addLayout(self.playerLayout)
        self.mainLayout.addWidget(self.notificationList)
        
        #Media player widget
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

       
        self.videoWidget = QVideoWidget()
        
        

       
        
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        #self.playerLayout.addLayout(unitsLayout)
        self.playerLayout.addWidget(self.videoWidget)
        
       
        
        self.subtitleLabel = QLabel()
        self.subtitleLabel.setFont(QFont('Arial', 15))
        self.playerLayout.addWidget(self.subtitleLabel)
        
        controlLayout = QHBoxLayout()

        controlLayout.addSpacing(10)
        #Player button
        self.startStopBtn = QPushButton()
        self.startStopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        controlLayout.addWidget(self.startStopBtn)
        controlLayout.addSpacing(10)
        
        #Player position
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderReleased.connect(self.scrollBarChanged)
        controlLayout.addWidget(self.positionSlider)
        
        self.timeLabel = QLabel("")
        controlLayout.addWidget(self.timeLabel)
        controlLayout.addSpacing(10)
        self.playerLayout.addLayout(controlLayout)
        
        self.setLayout(self.mainLayout)
        
        
        #Connect a bunch of signals
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.startStopBtn.clicked.connect(self.play)
        
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.startStopBtn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.startStopBtn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
    def humanize_time(self, secs):
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        return '%02d:%02d:%02d' % (hours, mins, secs)
        
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.timeLabel.setText(self.humanize_time(self.mediaPlayer.position()/1000))
        subtitle = self.loader.subtitleAtPosition(position/1000)
        print(subtitle)
        self.subtitleLabel.setText(subtitle[0] + " " + str(subtitle[3]))
        
        #Get Texts in this form:
        # 1. original value
        # 2. conversion
        # 3. relations
        # Create a list in the previous order and create list of the same size containing the icons (as pixmaps).
        # Example for reading a pixmap environmentImg = QPixmap.fromImage(QImage("./icon/environment.png"))
        # Create a CustomListItem with both lists as argument
        # Use this code:
        # myItem = CustomListItem(list1, list2)
        # for item in myItem.getListItems():
        #    self.notificationList.addItem(item)
        # self.notificationList.scrollToBottom()
    def scrollBarChanged(self):
        self.mediaPlayer.setPosition(self.positionSlider.value())

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def resizeEvent(self, event):
        
        self.resized.emit()
        result = super(MainWidget, self).resizeEvent(event)
        return result
        

        
class CustomListItem():
    def __init__(self, texts, icons):
        if len(texts) != len(icons):
            raise Exception("Size of texts list and size of icon list must be the same")
        
        self.items = []
        for index, text in enumerate(texts):
            item = QListWidgetItem()
            item.setText(text)
            item.setFont(QFont("Arial",20))
            item.setIcon(QIcon(icons[index].scaled(40,40)))        
            self.items.append(item)
    def getListItems(self):
        return self.items

        
        
        
