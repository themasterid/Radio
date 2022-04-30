import json
import sys
import threading
import time

import vlc
from PyQt5 import QtWidgets

from Radio_GUI import Ui_MainWindow


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.combo_list_radio.addItems(self.get_combo_list())
        self.ui.Button_Play.clicked.connect(self.playmusic)
        self.ui.Button_Stop.clicked.connect(self.stopmusic)
        self.ui.combo_list_radio.currentTextChanged.connect(self.playmusic)
        self.ui.horizontalSlider.valueChanged[int].connect(
            self.set_volume)

    def thread(my_func):
        def wrapper(*args, **kwargs):
            my_thread = threading.Thread(
                target=my_func, args=args, kwargs=kwargs)
            my_thread.start()
        return wrapper

    def play_or_stop(my_func):
        def wrapper(self):
            global stop_or_play
            stop_or_play = 0
            time.sleep(0.5)
            my_func(self)
        return wrapper

    @thread
    def playradio(self, canal):
        global stop_or_play, vlcMediaPlayer
        stop_or_play = 1
        vlcMediaPlayer = vlc.MediaPlayer(canal)
        vlcMediaPlayer.audio_set_volume(30)
        vlcMediaPlayer.play()
        while stop_or_play == 1:
            time.sleep(0.5)
        vlcMediaPlayer.stop()

    def set_volume(self, volume):
        vlcMediaPlayer.audio_set_volume(volume)

    def get_json(self):
        with open(
            'canals/radiochannels.json', 'r', encoding='utf-8'
        ) as read_json_file:
            return json.load(read_json_file)

    def get_combo_list(self):
        return [key for key, _ in self.get_json().items()]

    def get_list_radio(self):
        return [val for _, val in self.get_json().items()]

    @play_or_stop
    def playmusic(self):
        key_radio = self.ui.combo_list_radio.currentIndex()
        radio_now = self.get_list_radio()
        self.playradio(radio_now[key_radio])

    @play_or_stop
    def stopmusic(self):
        return

    def closeevent(self, event):
        self.stopmusic()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
