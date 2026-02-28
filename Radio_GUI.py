# -*- coding: utf-8 -*-

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMinimumSize(QtCore.QSize(500, 400))
        MainWindow.setMaximumSize(QtCore.QSize(700, 500))

        # Иконка
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("play.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)

        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Основной вертикальный layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # === ЗАГОЛОВОК ===
        self.title_label = QtWidgets.QLabel("🎵 Интернет Радио")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setMinimumHeight(50)
        main_layout.addWidget(self.title_label)

        # === ВЫБОР СТАНЦИИ ===
        self.combo_list_radio = QtWidgets.QComboBox()
        self.combo_list_radio.setObjectName("combo_list_radio")
        self.combo_list_radio.setMinimumHeight(45)
        main_layout.addWidget(self.combo_list_radio)

        # === КНОПКИ УПРАВЛЕНИЯ ===
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.Button_Play = QtWidgets.QPushButton("▶ Play")
        self.Button_Play.setObjectName("playButton")
        self.Button_Play.setMinimumHeight(60)
        buttons_layout.addWidget(self.Button_Play)

        self.Button_Stop = QtWidgets.QPushButton("⏹ Stop")
        self.Button_Stop.setObjectName("stopButton")
        self.Button_Stop.setMinimumHeight(60)
        buttons_layout.addWidget(self.Button_Stop)

        main_layout.addLayout(buttons_layout)

        # === ГРОМКОСТЬ ===
        volume_container = QtWidgets.QWidget()
        volume_layout = QtWidgets.QVBoxLayout(volume_container)
        volume_layout.setContentsMargins(0, 0, 0, 0)
        volume_layout.setSpacing(10)

        self.volume_label = QtWidgets.QLabel("🔊 Громкость")
        self.volume_label.setObjectName("volumeLabel")
        self.volume_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        volume_layout.addWidget(self.volume_label)

        self.horizontalSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("volumeSlider")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setMinimumHeight(30)
        volume_layout.addWidget(self.horizontalSlider)

        main_layout.addWidget(volume_container)

        # === ИНФОРМАЦИЯ ===
        self.info_label = QtWidgets.QLabel("Готово к работе")
        self.info_label.setObjectName("infoLabel")
        self.info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_label.setMinimumHeight(30)
        main_layout.addWidget(self.info_label)

        # Пружина
        main_layout.addStretch()

        MainWindow.setCentralWidget(self.centralwidget)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Радио"))
