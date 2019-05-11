from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QStyle, QWidget, QGraphicsTextItem, QGraphicsView, QGraphicsScene
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtCore import  QDir, Qt, QUrl, QSizeF, QRectF, QPointF
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage          


class MainWindow(QMainWindow):

    #The subtitlePath is optional, if it is none we can run a speech recognition instead.
    def __init__(self, videoPath = None, subtitlePath = None):
        super().__init__()
        if videoPath == None:
            print("Videopath may not be none")
            #raise Exception("Videopath may not be none!")
        self.videoPath = videoPath
        self.subtitlePath = subtitlePath
    
        self.initUI()

    def initUI(self):
       
        self.resize(400,400)
        
        self.setWindowTitle("Automatisches Einheiten in Relationssetzungsprogramm")
        centralWidget = MainWidget()
        self.setCentralWidget(centralWidget)
        
        centralWidget.openVideo(self.videoPath)
            
       
        
class MainWidget(QWidget):
    resized = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def openVideo(self,path):
        print(path)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(str(path))))

        
     
    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.playerLayout = QVBoxLayout()


        
        self.mainLayout.addLayout(self.playerLayout)

        
        #Media player widget
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

       
        self.videoWidget = QVideoWidget()
        
        
        #Units label
        unitsLayout = QHBoxLayout()
        
        unitsImg = QPixmap.fromImage(QImage("./icon/index.jpeg"))
        self.unitsIcon = QLabel()
        self.unitsIcon.setPixmap(unitsImg.scaled(40,40))
        
        self.topUnits = QLabel("Units:")
        unitsLayout.addWidget(self.unitsIcon)
        unitsLayout.addWidget(self.topUnits)
       
        
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.playerLayout.addLayout(unitsLayout)
        self.playerLayout.addWidget(self.videoWidget)
        
        relationLayout = QHBoxLayout()
        
        #Icons and Labels
        environmentImg = QPixmap.fromImage(QImage("./icon/environment.png"))
        self.environmentIcon = QLabel()
   
        self.environmentIcon.setPixmap(environmentImg.scaled(40,40))
        self.environmentText = QLabel("Text")
        
        militaryImg = QPixmap.fromImage(QImage("./icon/military.png"))
        self.militaryIcon = QLabel()
        self.militaryIcon.setPixmap(militaryImg.scaled(40,40))
        self.militaryText = QLabel("Text")
        
        socialImg = QPixmap.fromImage(QImage("./icon/social.png"))
        self.socialIcon = QLabel()
        self.socialIcon.setPixmap(socialImg.scaled(40,40))
        self.socialText = QLabel("Text")
        
        relationLayout.addWidget(self.environmentIcon)
        relationLayout.addWidget(self.environmentText)
        relationLayout.addStretch(1)
        relationLayout.addWidget(self.militaryIcon)
        relationLayout.addWidget(self.militaryText)
        relationLayout.addStretch(1)
        relationLayout.addWidget(self.socialIcon)
        relationLayout.addWidget(self.socialText)
        
        self.playerLayout.addLayout(relationLayout)
        
        controlLayout = QHBoxLayout()
        #Player button
        self.startStopBtn = QPushButton()
        self.startStopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        controlLayout.addWidget(self.startStopBtn)
        
        
        #Player position
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        controlLayout.addWidget(self.positionSlider)
        
        self.timeLabel = QLabel("")
        controlLayout.addWidget(self.timeLabel)
        
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

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def resizeEvent(self, event):
        
        self.resized.emit()
        result = super(MainWidget, self).resizeEvent(event)
        return result
        

        

        
        
        
