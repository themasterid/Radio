# Play Radio for All on Python 3.6 windows
import sys
import time
import threading
import vlc
import json
from PyQt5 import QtWidgets

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from Radio_GUI import Ui_MainWindow
from radiolist import combo_list_radio


def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper


@thread
def playradio(canal):
    global stop_or_play
    stop_or_play = 1
    vlcMediaPlayer = vlc.MediaPlayer(canal)
    vlcMediaPlayer.play()
    while stop_or_play == 1:
        time.sleep(0.7)
    vlcMediaPlayer.stop()


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.combo_list_radio.addItems(combo_list_radio)
        self.ui.Button_Play.clicked.connect(self.PlayMusic)
        self.ui.Button_Stop.clicked.connect(self.StopMusic)
        self.ui.combo_list_radio.currentTextChanged.connect(self.PlayMusic)
        self.ui.horizontalSlider.valueChanged[int].connect(self.get_valume)

    def get_valume(self, value):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.GetMute()
        volume.GetMasterVolumeLevel()
        volume.GetVolumeRange()
        volume.SetMasterVolumeLevel(value, None)

    def PlayMusic(self):
        global stop_or_play
        stop_or_play = 0
        time.sleep(1)
        key_radio = str(self.ui.combo_list_radio.currentText())
        with open('canals/radiochannels.json', 'r', encoding='utf-8') as read_json_file:
            data_json = json.load(read_json_file)
            read_json_file.close()
        playradio(data_json[key_radio])

    def StopMusic(self):
        global stop_or_play
        stop_or_play = 0
        time.sleep(1)

    def closeEvent(self, event):
        self.StopMusic()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
