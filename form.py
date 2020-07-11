# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from tinytag import TinyTag
import pygame, json, random
from tkinter import filedialog

add_num = 0
play_number = 0
class Ui_wema(object):
    def play(self, num):
        global current_played
        current_played = num
        with open("assets\\lib\\library.json",'r') as f:
            json_object = json.load(f)
        directory = json_object[str(num)]
        directory = directory[1]
        print(directory)
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(0)
        tag = TinyTag.get(directory, image=True)
        image_data = tag.get_image()
        if image_data:
            with open("assets/tmp/album_art.jpg", "wb") as f:
                f.write(image_data)
            covdir = "assets/tmp/album_art.jpg"
        else:
            covdir = "assets/images/cover.jpg"
        self.retranslateUi(wema, directory)
        self.cover.setStyleSheet("QWidget #cover{image: url(\"" + f"{covdir}" + "\");}")
    def prevf(self):
        self.play(current_played - 1)
    def nextf(self):
        self.play(current_played + 1)
    def add_music(self):
        global add_num
        directory = filedialog.askopenfilename(initialdir = "/",title = "Select a music",filetypes = (("wav fil","*.wav"),("mp3 fls","*.mp3")))
        tag = TinyTag.get(directory)
        if tag.title:
            data = tag.title
        else:
            data = os.path.splitext(os.path.basename(directory))[0]
        with open("assets\\lib\\library.json",'r+') as f:
            x = json.load(f)
            x[add_num] = [data, directory]
            f.seek(0)
            f.truncate()
            json.dump(x, f)
        f.close()
        self.listWidget.addItem(tag.title)
        print(self.listWidget.itemClicked)
        add_num += 1

        return
        

    def addPL(self,  x):
        self.x = QtWidgets.QWidget()
        self.x.setObjectName(f"{x}")
        self.playlists.addTab(self.x, "jkhjkhjkhjk")
        #self.playlists.setTabText(self.playlists.indexOf(self.x), _translate("wema", f"{x}"))


    def setupUi(self, wema):
        wema.setObjectName("wema")
        wema.resize(520, 720)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/icon/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        wema.setWindowIcon(icon)
        wema.setToolTip("")
        wema.setStyleSheet("")
        self.top = QtWidgets.QFrame(wema)
        self.top.setGeometry(QtCore.QRect(0, 0, 520, 320))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.top.setFont(font)
        self.top.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.top.setObjectName("top")
        self.songname = QtWidgets.QLabel(self.top)
        self.songname.setGeometry(QtCore.QRect(10, 260, 351, 30))
        font = QtGui.QFont()
        font.setFamily("Fantezy")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.songname.setFont(font)
        self.songname.setObjectName("songname")
        self.timebar = QtWidgets.QProgressBar(self.top)
        self.timebar.setGeometry(QtCore.QRect(100, 305, 405, 10))
        self.timebar.setProperty("value", 64)
        self.timebar.setTextVisible(False)
        self.timebar.setInvertedAppearance(True)
        self.timebar.setObjectName("timebar")
        self.time = QtWidgets.QLabel(self.top)
        self.time.setGeometry(QtCore.QRect(10, 300, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.time.setFont(font)
        self.time.setObjectName("time")
        self.cover = QtWidgets.QWidget(self.top)
        self.cover.setGeometry(QtCore.QRect(140, 5, 240, 240))
        self.cover.setStyleSheet("QWidget #cover{image: url(\"assets/images/cover.jpg\");}")
        self.cover.setObjectName("cover")
        self.volume = QtWidgets.QToolButton(self.top)
        self.volume.setGeometry(QtCore.QRect(350, 260, 30, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/icon/volume.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.volume.setIcon(icon1)
        self.volume.setIconSize(QtCore.QSize(30, 30))
        self.volume.setAutoRaise(True)
        self.volume.setObjectName("volume")
        self.progressBar = QtWidgets.QProgressBar(self.top)
        self.progressBar.setGeometry(QtCore.QRect(390, 265, 118, 20))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setObjectName("progressBar")
        self.controlers = QtWidgets.QFrame(wema)
        self.controlers.setGeometry(QtCore.QRect(0, 320, 520, 60))
        self.controlers.setObjectName("controlers")
        self.play_pause = QtWidgets.QToolButton(self.controlers)
        self.play_pause.setGeometry(QtCore.QRect(10, 5, 50, 50))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.play_pause.setFont(font)
        self.play_pause.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.play_pause.setAutoFillBackground(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/icon/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause.setIcon(icon2)
        self.play_pause.setIconSize(QtCore.QSize(50, 50))
        self.play_pause.setAutoRepeat(True)
        self.play_pause.setAutoExclusive(True)
        self.play_pause.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.play_pause.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.play_pause.setAutoRaise(True)
        self.play_pause.setObjectName("play_pause")
        self.stop = QtWidgets.QToolButton(self.controlers)
        self.stop.setGeometry(QtCore.QRect(65, 11, 40, 40))
        self.stop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assets/icon/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon3)
        self.stop.setIconSize(QtCore.QSize(40, 40))
        self.stop.setAutoRaise(True)
        self.stop.setObjectName("stop")
        self.next = QtWidgets.QToolButton(self.controlers)
        self.next.setGeometry(QtCore.QRect(145, 11, 40, 40))
        self.next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("assets/icon/next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon4)
        self.next.setIconSize(QtCore.QSize(40, 40))
        self.next.setAutoRaise(True)
        self.next.setObjectName("next")
        self.prev = QtWidgets.QToolButton(self.controlers)
        self.prev.setGeometry(QtCore.QRect(105, 11, 40, 40))
        self.prev.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("assets/icon/prev.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prev.setIcon(icon5)
        self.prev.setIconSize(QtCore.QSize(40, 40))
        self.prev.setAutoRaise(True)
        self.prev.setObjectName("prev")
        self.repeat = QtWidgets.QToolButton(self.controlers)
        self.repeat.setGeometry(QtCore.QRect(420, 11, 40, 40))
        self.repeat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("assets/icon/repeat.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.repeat.setIcon(icon6)
        self.repeat.setIconSize(QtCore.QSize(40, 40))
        self.repeat.setAutoRaise(True)
        self.repeat.setObjectName("repeat")
        self.shuffle = QtWidgets.QToolButton(self.controlers)
        self.shuffle.setGeometry(QtCore.QRect(470, 11, 40, 40))
        self.shuffle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("assets/icon/shuffle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shuffle.setIcon(icon7)
        self.shuffle.setIconSize(QtCore.QSize(40, 40))
        self.shuffle.setAutoRaise(True)
        self.shuffle.setObjectName("shuffle")


        self.playlists = QtWidgets.QTabWidget(wema)
        self.playlists.setGeometry(QtCore.QRect(0, 380, 520, 300))
        self.playlists.setObjectName("playlists")

        self.recent = QtWidgets.QWidget()
        self.recent.setObjectName("recent")

        self.listWidget = QtWidgets.QListWidget(self.recent)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 520, 273))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemDoubleClicked.connect(lambda: self.play(self.listWidget.currentRow()))

        self.playlists.addTab(self.recent, "")


        self.queue = QtWidgets.QWidget()
        self.queue.setObjectName("queue")
        self.playlists.addTab(self.queue, "")



        x="p1"
        y="p2"
        self.addPL(x)
        self.addPL(y)

       


        self.bottom = QtWidgets.QFrame(wema)
        self.bottom.setGeometry(QtCore.QRect(0, 680, 520, 40))
        self.bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom.setObjectName("bottom")
        self.addlib = QtWidgets.QToolButton(self.bottom)
        self.addlib.setGeometry(QtCore.QRect(440, 5, 30, 30))
        self.addlib.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addlib.setAcceptDrops(True)
        self.addlib.setAutoFillBackground(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("assets/icon/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addlib.setIcon(icon8)
        self.addlib.setIconSize(QtCore.QSize(30, 30))
        self.addlib.setObjectName("addlib")
        self.totalbtn = QtWidgets.QToolButton(self.bottom)
        self.totalbtn.setGeometry(QtCore.QRect(10, 5, 30, 30))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("assets/icon/music.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.totalbtn.setIcon(icon9)
        self.totalbtn.setIconSize(QtCore.QSize(30, 30))
        self.totalbtn.setAutoRaise(True)
        self.totalbtn.setObjectName("totalbtn")
        self.removelib = QtWidgets.QToolButton(self.bottom)
        self.removelib.setGeometry(QtCore.QRect(480, 5, 30, 30))
        self.removelib.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("assets/icon/remove.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removelib.setIcon(icon10)
        self.removelib.setIconSize(QtCore.QSize(30, 30))
        self.removelib.setAutoRaise(True)
        self.removelib.setObjectName("removelib")


        
        
        self.retranslateUi(wema)
        self.playlists.setCurrentIndex(0)
        self.play_pause.clicked.connect(pp)
        self.addlib.clicked.connect(self.add_music)
        self.removelib.clicked.connect(self.removelib.deleteLater)
        self.totalbtn.toggled['bool'].connect(self.totalbtn.update)
        self.stop.clicked.connect(stop)
        self.prev.clicked.connect(self.prevf)
        self.next.clicked.connect(self.nextf)
        self.shuffle.toggled['bool'].connect(self.shuffle.animateClick)
        self.repeat.toggled['bool'].connect(self.repeat.animateClick)
        QtCore.QMetaObject.connectSlotsByName(wema)








    def retranslateUi(self, wema, dire =""):
        if dire:
            print(dire)
            tag = TinyTag.get(dire)
            if tag.title:
                title = tag.title 
            else:
                title = os.path.splitext(os.path.basename(directory))[0]
            if tag.artist:
                title += " - " + tag.artist
            self.songname.setText(title)
            self.time.setText(f"{int(tag.duration / 3600):02d}:{int(tag.duration / 60):02d}:{int(tag.duration % 60):02d}")
        else:
            _translate = QtCore.QCoreApplication.translate
            wema.setWindowTitle(_translate("wema", "wema player"))
            self.songname.setText(_translate("wema", "song name"))
            self.time.setText(_translate("wema", "00:00:00"))
            self.volume.setText(_translate("wema", "voulume"))
            self.play_pause.setText(_translate("wema", "play"))
            self.stop.setText(_translate("wema", "stop"))
            self.next.setText(_translate("wema", "next"))
            self.prev.setText(_translate("wema", "prev"))
            self.repeat.setText(_translate("wema", "repeat"))
            self.shuffle.setText(_translate("wema", "shuffle"))
            self.playlists.setTabText(self.playlists.indexOf(self.recent), _translate("wema", "recently played"))
            self.playlists.setTabText(self.playlists.indexOf(self.queue), _translate("wema", "Queue"))
            self.addlib.setText(_translate("wema", "+"))
            self.totalbtn.setText(_translate("wema", "total"))
            self.removelib.setText(_translate("wema", "-"))

 

        
def remove_library(name):
    with open("assets\\file\\library.json",'a') as f:
        data=json.load(f)
    del data[name]
    with open("assets\\file\\library.json",'w') as f:
        json.dump(data,f)

def add_playlist(play_list_name,**names):
    data=json.load("assets\\file\\library.json")
    plist_data={}
    #with open("assets\\file\\{}.json".format(play_list_name),'w') as f:
        

    
    # if shuffle:
    #     pass
    #     rand = rand
    #     directory = json_object[list_object[rand]]
    # if repeat_one:
    #     play_number = 0
    #     play(name)
    # if repeat:
    #     play_number = 0
    #     num += 1
    #     directory = json_object[list_object[num]]

def pp():
    global play_number
    if play_number % 2 == 0:
        pygame.mixer.music.pause()
    elif play_number % 2 == 1:
        pygame.mixer.music.unpause()
    play_number+=1
    return

def stop():
    global play_number
    pygame.mixer.music.stop()
    play_number = 0

if __name__ == "__main__":
    import sys
    pygame.init()
    pygame.mixer.init()
    app = QtWidgets.QApplication(sys.argv)
    wema = QtWidgets.QWidget()
    ui = Ui_wema()
    ui.setupUi(wema)
    wema.show()
    sys.exit(app.exec_())


