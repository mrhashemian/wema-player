# This Python file uses the following encoding: utf-8
import sys,pygame
import os
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class wema(QWidget):
    def __init__(self):
        super(wema, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

def play(directory):
    pygame.mixer.music.load(directory)
    pygame.mixer.music.play(0)
def pause():
    pygame.mixer.music.pause()
def unpause():
    pygame.mixer.music.unpause()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    app = QApplication([])
    widget = wema()
    widget.show()
    directory="C:\\Users\\Lenovo\\Documents\\GitHub\\wema-player\\assets\\music"
    os.chdir(directory)
    song_list=os.listdir(directory)
    play(song_list[0])
    sys.exit(app.exec_())
