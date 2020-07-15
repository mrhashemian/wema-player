from PyQt5 import QtCore, QtGui, QtWidgets
from tinytag import TinyTag
import pygame, json, random, os, sys
from tkinter import filedialog

mute_number = 0
addmusic_num = 0
play_number = 0
pl_num = 1
tab_number=0
duration = 0 
# 0 : play once
# 1 : repeat current
# 2 : repeat list
# 3 : shuffle
repeat_flag= 0
def make_time(time):   
    return f"{int(time / 3600):02d}:{int(time / 60):02d}:{int(time % 60):02d}"
with open("assets\\lib\\x0.json",'w') as f:
    f.write("{}")
class mythread(QtCore.QThread):
    def run(self):
        global ui
        while True:
            if (pygame.mixer.music.get_pos()!=-1):
                ui.time.setText(make_time(pygame.mixer.music.get_pos()//1000))
                ui.time2.setText(make_time(duration - pygame.mixer.music.get_pos()//1000))
            for event in pygame.event.get():
                if event.type == SONG_END:
                    if repeat_flag == 1:
                        ui.repeatf()
                    elif repeat_flag == 2:
                        ui.nextf()
                    elif repeat_flag == 3:
                        ui.shufflef()
def repeat():
    global repeat_flag
    repeat_flag += 1
    repeat_flag %= 4
    if repeat_flag == 0:
        ui.s.setText("repeat once")
    if repeat_flag == 1:
        ui.s.setText("repeat current")
    if repeat_flag == 2:
        ui.s.setText("repeat list")
    if repeat_flag == 3:
        ui.s.setText("shuffle")
class Ui_wema(object):
    def play(self, num):
        global SONG_END
        print(num)
        SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(SONG_END)
        self.threads=mythread()
        self.threads.start()
        global current_played,play_number
        current_played = num
        with open(f"assets\\lib\\x{self.playlists.currentIndex()}.json",'r+') as f:
            json_object = json.load(f)
        directory = json_object[str(num)]
        directory = directory[1]
        print(directory)
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(0)
        tag = TinyTag.get(directory, image=True)
        image_data = tag.get_image()
        global duration
        duration = tag.duration
        if image_data:
            with open("assets/tmp/album_art.jpg", "wb") as f:
                f.write(image_data)
            covdir = "assets/tmp/album_art.jpg"
        else:
            covdir = "assets/images/cover.jpg"
        self.retranslateUi(wema, directory)
        self.cover.setStyleSheet("QWidget #cover{image: url(\"" + f"{covdir}" + "\");}")
    def prevf(self):
        print(pygame.mixer.music.get_pos())
        if current_played>0:
            self.play(current_played - 1)
        else:
            print("first music")
    def nextf(self):
        print(pygame.mixer.music.get_pos())
        if current_played<(addmusic_num - 1):
            self.play(current_played + 1)
        else:
            self.play(0)
    def volume_up(self):
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.100)
        self.sound.setText(str(int(pygame.mixer.music.get_volume() * 100)) + "%")
    def volume_down(self):
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.100)
        self.sound.setText(str(int(pygame.mixer.music.get_volume() * 100)) + "%")
    def mute(self):
        global mute_number
        if mute_number % 2 == 0:
            pygame.mixer.music.set_volume(0)
            self.sound.setText("muted")
        else:
            pygame.mixer.music.set_volume(0.5)
            self.sound.setText("unmute")
        mute_number += 1
        mute_number %= 2
    def shufflef(self):
        next_song = random.choice(range(0, addmusic_num))
        while next_song == current_played:
            next_song = random.choice(range(0, addmusic_num))
        print(next_song)
        self.play(next_song)
    def repeatf(self):
        self.play(current_played)
    def add_music(self):
        directory = filedialog.askopenfilename(initialdir = "/",title = "Select a music",filetypes = (("wav fil","*.wav"),("mp3 fls","*.mp3")))
        #directory  = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        tag = TinyTag.get(directory)
        if tag.title:
            data = tag.title
        else:
            data = os.path.splitext(os.path.basename(directory))[0]
        global addmusic_num
        with open(f"assets\\lib\\x{self.playlists.currentIndex()}.json",'r+') as f:
            x = json.load(f)
            addmusic_num = len(x)
            x[addmusic_num] = [data, directory]
            f.seek(0)
            f.truncate()
            json.dump(x, f)
        f.close()
        temp = "self.x{}.addItem(tag.title)".format(self.playlists.currentIndex())
        exec(temp)
    def remove_music(self):
        temp = "self.x{}.currentRow()".format(self.playlists.currentIndex())
        remove_num = exec(temp)
        print(remove_num)
        with open(f"assets\\lib\\x{self.playlists.currentIndex()}.json",'r+') as f:
            x = json.load(f)
            x.pop(str(remove_num))
            f.seek(0)
            f.truncate()
            json.dump(x, f)
        f.close()
        temp = "self.x{}.takeItem({})".format(self.playlists.currentIndex(), self.playlists.currentIndex())
        exec(temp)
        exec("print(self.x{}.itemClicked)".format(self.playlists.currentIndex()))
    def addPL(self,  i):
        with open(f"assets\\lib\\x{i}.json",'w') as f:
            f.write("{}")
        self.obj = QtWidgets.QTabWidget()
        self.obj.setObjectName(f"x{i}")
        temp = "self.x{} = QtWidgets.QListWidget(self.obj)".format(i)
        exec(temp)
        temp = "self.x{}.setGeometry(QtCore.QRect(0, 0, 520, 273))".format(i)
        exec(temp)
        temp = "self.x{}.setObjectName('list widget')".format(i)
        exec(temp)
        self.playlists.addTab(self.obj, f"pl{i}")
        global pl_num
        pl_num += 1
        global tab_number
        tab_number+=1
        temp2 = "self.x{}.itemDoubleClicked.connect(lambda: ui.play(ui.x{}.currentRow()))".format(tab_number,tab_number)
        exec(temp2)
        print(pl_num)
    def removePL(self):
        os.remove(f"assets\\lib\\x{self.playlists.currentIndex()}.json")
        self.playlists.hide(self.playlists.currentIndex())
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
    
        
        self.time = QtWidgets.QLabel(self.top)
        self.time.setGeometry(QtCore.QRect(10, 300, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.time.setFont(font)
        self.time.setObjectName("time")

        self.time2 = QtWidgets.QLabel(self.top)
        self.time2.setGeometry(QtCore.QRect(110, 300, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.time2.setFont(font)
        self.time2.setObjectName("time")

        self.time3 = QtWidgets.QLabel(self.top)
        self.time3.setGeometry(QtCore.QRect(210, 300, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.time3.setFont(font)
        self.time3.setObjectName("time")

        self.sound = QtWidgets.QLabel(self.top)
        self.sound.setGeometry(QtCore.QRect(305, 300, 80, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.sound.setFont(font)
        self.sound.setObjectName("sound")

        self.s = QtWidgets.QLabel(self.top)
        self.s.setGeometry(QtCore.QRect(395, 300, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.s.setFont(font)
        self.s.setObjectName("s")

        self.cover = QtWidgets.QWidget(self.top)
        self.cover.setGeometry(QtCore.QRect(140, 5, 240, 240))
        self.cover.setStyleSheet("QWidget #cover{image: url(\"assets/images/cover.jpg\");}")
        self.cover.setObjectName("cover")
        
        self.volume = QtWidgets.QToolButton(self.top)
        self.volume.setGeometry(QtCore.QRect(400, 260, 30, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/icon/volume.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.volume.setIcon(icon1)
        self.volume.setIconSize(QtCore.QSize(30, 30))
        self.volume.setAutoRaise(True)
        self.volume.setObjectName("volume")
        self.volume.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.vup = QtWidgets.QToolButton(self.top)
        self.vup.setGeometry(QtCore.QRect(440, 260, 30, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/icon/plus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.vup.setIcon(icon1)
        self.vup.setIconSize(QtCore.QSize(30, 30))
        self.vup.setAutoRaise(True)
        self.vup.setObjectName("volume")
        self.vup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.vdown = QtWidgets.QToolButton(self.top)
        self.vdown.setGeometry(QtCore.QRect(480, 260, 30, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/icon/minus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.vdown.setIcon(icon1)
        self.vdown.setIconSize(QtCore.QSize(30, 30))
        self.vdown.setAutoRaise(True)
        self.vdown.setObjectName("volume")
        self.vdown.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        

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
        self.x0 = QtWidgets.QListWidget(self.recent)
        self.x0.setGeometry(QtCore.QRect(0, 0, 520, 273))
        self.x0.setObjectName("listWidget")
        self.playlists.addTab(self.recent, "")

        
        self.x0.itemDoubleClicked.connect(lambda: self.play(self.x0.currentRow()))

       


        self.bottom = QtWidgets.QFrame(wema)
        self.bottom.setGeometry(QtCore.QRect(0, 680, 520, 40))
        self.bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom.setObjectName("bottom")
        

        self.addmusic = QtWidgets.QToolButton(self.bottom)
        self.addmusic.setGeometry(QtCore.QRect(10, 5, 30, 30))
        self.addmusic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addmusic.setAcceptDrops(True)
        self.addmusic.setAutoFillBackground(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("assets/icon/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addmusic.setIcon(icon8)
        self.addmusic.setIconSize(QtCore.QSize(30, 30))
        self.addmusic.setObjectName("addmusic")
        
        self.removemusic = QtWidgets.QToolButton(self.bottom)
        self.removemusic.setGeometry(QtCore.QRect(50, 5, 30, 30))
        self.removemusic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("assets/icon/remove.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removemusic.setIcon(icon10)
        self.removemusic.setIconSize(QtCore.QSize(30, 30))
        self.removemusic.setAutoRaise(True)
        self.removemusic.setObjectName("removemusic")

        self.totalbtn = QtWidgets.QToolButton(self.bottom)
        self.totalbtn.setGeometry(QtCore.QRect(245, 5, 30, 30))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("assets/icon/music.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.totalbtn.setIcon(icon9)
        self.totalbtn.setIconSize(QtCore.QSize(30, 30))
        self.totalbtn.setAutoRaise(True)
        self.totalbtn.setObjectName("totalbtn")
        
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
        self.addlib.clicked.connect(lambda: self.addPL(pl_num))
        self.removelib.clicked.connect(self.removePL)
        self.addmusic.clicked.connect(self.add_music)
        self.removemusic.clicked.connect(self.remove_music)
        self.totalbtn.customContextMenuRequested.connect(self.totalbtn.deleteLater)
        self.stop.clicked.connect(stop)
        self.prev.clicked.connect(self.prevf)
        self.next.clicked.connect(self.nextf)
        self.shuffle.clicked.connect(repeat)
        self.vup.clicked.connect(self.volume_up)
        self.vdown.clicked.connect(self.volume_down)
        self.volume.clicked.connect(self.mute)
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
            time = tag.duration
            self.time3.setText(f"{int(time / 3600):02d}:{int(time / 60):02d}:{int(time % 60):02d}")       
        else:
            _translate = QtCore.QCoreApplication.translate
            wema.setWindowTitle(_translate("wema", "wema player"))
            self.songname.setText(_translate("wema", "song name"))
            self.time.setText(_translate("wema", "00:00"))
            self.time2.setText(_translate("wema", "00:00"))
            self.time3.setText(_translate("wema", "00:00"))
            self.s.setText(_translate("wema", "repeat once"))
            self.volume.setText(_translate("wema", "voulume"))
            self.play_pause.setText(_translate("wema", "play"))
            self.stop.setText(_translate("wema", "stop"))
            self.next.setText(_translate("wema", "next"))
            self.prev.setText(_translate("wema", "prev"))
            self.shuffle.setText(_translate("wema", "shuffle"))
            self.playlists.setTabText(self.playlists.indexOf(self.recent), _translate("wema", "Library"))
            self.addmusic.setText(_translate("wema", "+"))
            self.removemusic.setText(_translate("wema", "-"))
            self.totalbtn.setText(_translate("wema", "total"))
            self.addlib.setText(_translate("wema", "+"))
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
    global app
    app = QtWidgets.QApplication(sys.argv)
    wema = QtWidgets.QWidget()
    global ui
    ui = Ui_wema()
    ui.setupUi(wema)
    wema.show()
    sys.exit(app.exec_())