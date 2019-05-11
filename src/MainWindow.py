from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QStyle, QWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl



class MainWindow(QMainWindow):

    #The subtitlePath is optional, if it is none we can run a speech recognition instead.
    def __init__(self, videoPath = None, subtitlePath = None):
        super().__init__()
        self.initUI()
        if videoPath == None:
            print("Videopath may not be none")
            raise Exception("Videopath may not be none!")
        self.videoPath = videoPath
        self.subtitlePath = subtitlePath
    
    def initUI(self):
       
        
        
        self.setWindowTitle("Automatisches Einheiten in Relationssetzungsprogramm")
        centralWidget = MainWidget()
        self.setCentralWidget(centralWidget)
       
        
class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
     
    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.playerLayout = QVBoxLayout()


        
        self.mainLayout.addLayout(self.playerLayout)

        
        #Media player widet
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget();
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        self.playerLayout.addWidget(self.videoWidget)
        
        controlLayout = QHBoxLayout()
        #Player button
        self.startStopBtn = QPushButton()
        self.startStopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        controlLayout.addWidget(self.startStopBtn)
        
        #Player position
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        controlLayout.addWidget(self.positionSlider)
        
        self.playerLayout.addLayout(controlLayout)
        
        self.setLayout(self.mainLayout)
        
        
        #Connect a bunch of signals
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    
        
        
        
