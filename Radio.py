# Play Radio for All on Python 3.9.1 windows
import sys
import time
import threading
import vlc
import json
from PyQt5 import QtWidgets

from Radio_GUI import Ui_MainWindow


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)        
        self.ui.combo_list_radio.addItems(self.get_combo_list())      
        self.ui.Button_Play.clicked.connect(self.PlayMusic)
        self.ui.Button_Stop.clicked.connect(self.StopMusic)
        self.ui.combo_list_radio.currentTextChanged.connect(self.PlayMusic)
        vols = self.ui.horizontalSlider.valueChanged[int].connect(self.set_volume)     
    
    def thread(my_func):
        def wrapper(*args, **kwargs):
            my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
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
        vlcMediaPlayer.audio_set_volume(50)
        vlcMediaPlayer.play()
        while stop_or_play == 1:
            time.sleep(0.5)
        vlcMediaPlayer.stop()

    def set_volume(self, volume):
        vlcMediaPlayer.audio_set_volume(volume)

    def get_json(self):
        with open('canals/radiochannels.json', 'r', encoding='utf-8') as read_json_file:
            data_json = json.load(read_json_file)
            read_json_file.close()
        return data_json

    def get_combo_list(self):
        combo_list_radio = []   
        for key, _ in self.get_json().items():
            combo_list_radio.append(key)
        return combo_list_radio
    
    def get_list_radio(self):        
        combo_keys_radio = []   
        for _, val in self.get_json().items():
            combo_keys_radio.append(val)        
        return combo_keys_radio
    
    @play_or_stop
    def PlayMusic(self):
        key_radio = self.ui.combo_list_radio.currentIndex() 
        radio_now = self.get_list_radio()
        self.playradio(radio_now[key_radio])

    @play_or_stop
    def StopMusic(self):
        return

    def closeEvent(self, event):
        self.StopMusic()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
