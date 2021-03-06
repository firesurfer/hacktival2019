from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QStyle, QWidget, QGraphicsTextItem, QGraphicsView, QGraphicsScene, QSpacerItem, QListWidget, QListWidgetItem, QLineEdit
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtCore import  QDir, Qt, QUrl, QSizeF, QRectF, QPointF, QSize
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon, QBrush, QColor
import os
from time import sleep
from pathlib import Path
from Downloader import SubscriptionDownloader
from LoadIcons import IconLoader
from converter import Converter

class MainWindow(QMainWindow):

    #The subtitlePath is optional, if it is none we can run a speech recognition instead.
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
    
        self.initUI()

    def initUI(self):
       
        self.resize(1500,800)
        
        self.setWindowTitle("How Much Is That?         ")
        centralWidget = MainWidget(self.loader)
        self.setCentralWidget(centralWidget)
       
    def mute(self):
        self.centralWidget().mute()

    def enableSubtitles(self):
        self.centralWidget().enableSubtitles()
      

class MainWidget(QWidget):
    resized = QtCore.pyqtSignal()
    def __init__(self,args, parent=None):
        super().__init__(parent)
        self.args = args
        self.iconLoader = IconLoader()
        self.initUI()
        self.conv = Converter()
        self.previousSub = ""
        self.loadVideo(Path(args.url))

    def getIconLoader(self):
        return self.iconLoader

    def openVideo(self,path):
        print(path)
        path = os.path.abspath(path)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(str(path))))

    def loadVideo(self,url):
        self.loader = SubscriptionDownloader(Path(url))
        self.loader.download()
        while not self.loader.downloadFinished():
            sleep(1)
        print("Adding no offset")
        self.loader.process()
        self.openVideo(self.loader.videoPath())

    def mute(self):
        self.mediaPlayer.setVolume(0)   
    def enableSubtitles(self):
        self.subtitleLabel.setHidden(False)
    
    def initUI(self):


        self.mainLayout = QHBoxLayout()
        self.notificationList = QListWidget()
        self.notificationList.setMinimumWidth(450)
        self.notificationList.setMaximumWidth(500)
        self.notificationList.setIconSize(QSize(40,40))
        self.playerLayout = QVBoxLayout()
        
        self.searchBtn = QPushButton("...")
        self.searchText = QLineEdit(self)
        self.searchText.setVisible(False)
        self.loadButton = QPushButton("Load Video")
        self.loadButton.setVisible(False)
       

        
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
        self.subtitleLabel.setHidden(True)
        self.playerLayout.addWidget(self.subtitleLabel)
        
        controlLayout = QHBoxLayout()

        controlLayout.addSpacing(10)
        controlLayout.addWidget(self.searchBtn)
        self.searchBtn.clicked.connect(self.toggleShowLoadField)
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

        loadLayout = QHBoxLayout()

        loadLayout.addSpacing(10)
        loadLayout.addWidget(self.searchText)
        loadLayout.addWidget(self.loadButton)
        self.loadButton.clicked.connect(self.loadNewVideo)

        self.playerLayout.addLayout(controlLayout)
        self.playerLayout.addLayout(loadLayout)

        
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
        self.subtitleLabel.setText(subtitle[2] + " " + str(subtitle[3]))
        if self.previousSub == subtitle[2]:
            return
        self.previousSub = subtitle[2]
        if subtitle[3]:
            for sub in subtitle[3]:
                try:
                    elementsToShow = self.conv.what_to_show(sub)
                    print(elementsToShow)
                    listItem = CustomListItem(elementsToShow, self.iconLoader)
                    for item in listItem.getListItems():
                        self.notificationList.addItem(item)
                    self.notificationList.scrollToBottom()
                except:
                    print("Error converting value")
                    pass
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

    def toggleShowLoadField(self):
        self.loadButton.setVisible(self.loadButton.isHidden())
        self.searchText.setVisible(self.searchText.isHidden())

    def loadNewVideo(self):
        url = self.searchText.text()
        self.loadVideo(url)

        
class CustomListItem():
    def __init__(self, elements,icons):
        self.items = []
        i = 0
        for text,icon in elements:
           
                
            print(text)
            print(icon)
            item = QListWidgetItem()
            if i == 0:
                item.setBackground(QBrush(QColor(66,69,71)))
                item.setFont(QFont("Arial",20))
                item.setText(text)
                sizeHint = item.sizeHint()
                item.setSizeHint(QSize(sizeHint.width(),sizeHint.height()+80))
            elif i % 2:
                item.setBackground(QBrush(QColor(92,89,94)))  
                item.setFont(QFont("Arial",18))
                item.setText(" " + text)
                sizeHint = item.sizeHint()
                item.setSizeHint(QSize(sizeHint.width(),sizeHint.height()+65))
            else:
                item.setBackground(QBrush(QColor(92,85,94)))  
                item.setFont(QFont("Arial",18))
                item.setText(" " + text)
                sizeHint = item.sizeHint()
                item.setSizeHint(QSize(sizeHint.width(),sizeHint.height()+65))
            
            
           
            item.setIcon(QIcon(icons.getIcon(icon)))        
            self.items.append(item)
            i = i + 1
        spacerItem = QListWidgetItem()
        spacerItem.setFlags(Qt.NoItemFlags)
        self.items.append(spacerItem)
    def getListItems(self):
        return self.items

        


        
