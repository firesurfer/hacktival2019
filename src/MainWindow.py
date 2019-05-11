from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QStyle, QWidget, QGraphicsTextItem, QGraphicsView, QGraphicsScene
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtCore import  QDir, Qt, QUrl, QSizeF, QRectF, QPointF
from PyQt5 import QtCore



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
        # Graphics scene needed for overlay
        self.videoView = QGraphicsView()
        self.videoScene = QGraphicsScene()
        self.videoWidget = QGraphicsVideoItem()
        self.videoView.setScene(self.videoScene)

        
        self.videoScene.addItem(self.videoWidget)
        
        self.topOverlay = QLabel("Top")
        self.topOverlay.setAttribute(Qt.WA_TranslucentBackground)
        self.bottomOverlay = QLabel("Bottom")
        self.bottomOverlay.setAttribute(Qt.WA_TranslucentBackground)
        
        self.proxyTop = self.videoScene.addWidget(self.topOverlay)
        self.proxyTop.setPos(10,10)
        self.proxyBottom = self.videoScene.addWidget(self.bottomOverlay)
        self.proxyBottom.setPos(10,self.videoScene.height()-20)
        
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        self.playerLayout.addWidget(self.videoView)
        
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

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def resizeEvent(self, event):
        self.resized.emit()
        

        self.videoWidget.setSize(QSizeF(self.videoView.width(), self.videoView.width()))
        self.videoScene.setSceneRect(0,0,self.videoWidget.size().width(), self.videoWidget.size().height())

        self.videoWidget.setPos(0,0)
        self.videoWidget.setOffset(QPointF(0,0))
        self.proxyBottom.setPos(10,self.videoScene.height()-20)

        self.videoView.fitInView(QRectF(0,0,self.videoView.width(), self.videoView.width()), Qt.KeepAspectRatio)
        result = super(MainWidget, self).resizeEvent(event)
        return result
    
        
        
        
