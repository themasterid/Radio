#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import threading
import logging
import socket
from pathlib import Path
from urllib.parse import urlparse

import vlc
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

from Radio_GUI import Ui_MainWindow

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._init_vlc()
        self.radio_channels = self._load_channels()
        self.station_status = {}  # Статус доступности: {name: bool}

        self._setup_ui()
        self._apply_style()

        self._play_lock = threading.Lock()
        self.is_playing = False
        self._ui_ready = False

    def _init_vlc(self):
        vlc_args = ["--no-xlib", "--quiet"]
        try:
            self.vlc_instance = vlc.Instance(vlc_args)
            self.media_player = self.vlc_instance.media_player_new()
        except Exception as e:
            logger.error(f"Ошибка VLC: {e}")
            self.vlc_instance = None
            self.media_player = None

    def _load_channels(self) -> dict:
        json_path = Path("canals/radiochannels.json")
        if not json_path.exists():
            return {"R FM": "http://radio-holding.ru:9000/rfm"}
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _check_url_available(self, url: str, timeout: float = 2.0) -> bool:
        """Быстрая проверка доступности URL (без полной загрузки)"""
        try:
            parsed = urlparse(url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == "https" else 80)

            # Проверяем соединение с хостом
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, socket.error, OSError):
            return False
        except Exception:
            return False

    def _update_station_visual(self, station_name: str, is_available: bool):
        """Обновляет визуальное отображение станции в ComboBox"""
        combo = self.ui.combo_list_radio
        index = combo.findText(station_name)
        if index < 0:
            return

        if is_available:
            # Доступная: стандартный цвет
            combo.setItemData(index, QtGui.QColor("#c0caf5"), Qt.ItemDataRole.ForegroundRole)
            combo.setItemData(index, None, Qt.ItemDataRole.BackgroundRole)
            combo.setItemData(index, None, Qt.ItemDataRole.FontRole)
        else:
            # Недоступная: красный цвет + зачеркнутый
            combo.setItemData(index, QtGui.QColor("#f7768e"), Qt.ItemDataRole.ForegroundRole)
            combo.setItemData(index, QtGui.QColor("#24283b"), Qt.ItemDataRole.BackgroundRole)

            font = combo.itemData(index, Qt.ItemDataRole.FontRole) or QtGui.QFont()
            font.setStrikeOut(True)
            font.setItalic(True)
            combo.setItemData(index, font, Qt.ItemDataRole.FontRole)

    def _check_stations_availability(self):
        """Фоновая проверка доступности всех станций"""
        logger.info("Проверка доступности радиостанций...")

        for name, url in self.radio_channels.items():
            # Пропускаем проверку если уже есть статус
            if name in self.station_status:
                continue

            is_available = self._check_url_available(url)
            self.station_status[name] = is_available

            # Обновляем UI в главном потоке
            QtCore.QMetaObject.invokeMethod(
                self,
                "_update_station_visual",
                Qt.ConnectionType.QueuedConnection,
                QtCore.Q_ARG(str, name),
                QtCore.Q_ARG(bool, is_available),
            )

            status = "✅" if is_available else "❌"
            logger.info(f"{status} {name}")

            # Небольшая пауза между проверками
            QtCore.QThread.msleep(100)

        logger.info("Проверка завершена")

    def _apply_style(self):
        """Современный темный стиль"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1b26;
            }
            
            QWidget {
                background-color: #1a1b26;
                color: #a9b1d8;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #7aa2f7;
                background-color: transparent;
            }
            
            QLabel#volumeLabel {
                font-size: 14px;
                font-weight: bold;
                color: #bb9af7;
                background-color: transparent;
            }
            
            QLabel#infoLabel {
                font-size: 12px;
                color: #565f89;
                background-color: transparent;
            }
            
            QComboBox {
                background-color: #24283b;
                border: 2px solid #414868;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 13px;
                color: #c0caf5;
            }
            
            QComboBox:hover {
                border-color: #7aa2f7;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 35px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #7aa2f7;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #24283b;
                border: 2px solid #414868;
                border-radius: 10px;
                selection-background-color: #7aa2f7;
                selection-color: #1a1b26;
                padding: 5px;
            }
            
            QPushButton#playButton {
                background-color: #9ece6a;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                color: #1a1b26;
            }
            
            QPushButton#playButton:hover {
                background-color: #b4f9b8;
            }
            
            QPushButton#playButton:pressed {
                background-color: #73daca;
            }
            
            QPushButton#stopButton {
                background-color: #f7768e;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                color: #1a1b26;
            }
            
            QPushButton#stopButton:hover {
                background-color: #ff98a8;
            }
            
            QPushButton#stopButton:pressed {
                background-color: #e0af68;
            }
            
            QSlider::groove:horizontal {
                background: #414868;
                height: 8px;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #bb9af7;
                width: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #c3a5f7;
            }
            
            QSlider::sub-page:horizontal {
                background: #bb9af7;
                border-radius: 4px;
            }
            
            QStatusBar {
                background-color: #24283b;
                color: #565f89;
                border-top: 1px solid #414868;
            }
        """)

    def _setup_ui(self):
        """Настройка интерфейса"""
        self._apply_style()

        if self.radio_channels:
            # Добавляем станции в ComboBox
            for name in self.radio_channels.keys():
                self.ui.combo_list_radio.addItem(name)
                # По умолчанию считаем статус неизвестным (стандартный цвет)
                self.station_status[name] = None

        # Запускаем фоновую проверку доступности
        check_thread = threading.Thread(target=self._check_stations_availability, daemon=True)
        check_thread.start()

        self.ui.Button_Play.clicked.connect(self.play_music)
        self.ui.Button_Stop.clicked.connect(self.stop_music)
        self.ui.combo_list_radio.currentIndexChanged.connect(self.on_channel_changed)
        self.ui.horizontalSlider.valueChanged.connect(self.set_volume)

        self.set_volume(50)
        self.ui.statusbar.showMessage("🎵 Готово")

        self._ui_ready = True

    @staticmethod
    def _thread_worker(func):
        def wrapper(self, *args, **kwargs):
            thread = threading.Thread(target=func, args=(self, *args), kwargs=kwargs, daemon=True)
            thread.start()

        return wrapper

    def _stop_current_stream(self):
        try:
            if self.media_player and self.media_player.is_playing():
                self.media_player.stop()
                QtCore.QThread.msleep(100)
        except:
            pass
        self.is_playing = False

    @_thread_worker
    def _play_stream(self, url: str):
        with self._play_lock:
            try:
                self._stop_current_stream()

                if not self.media_player:
                    return

                media = self.vlc_instance.media_new(url)
                media.add_option(":network-caching=1000")
                media.add_option(":http-reconnect=1")

                self.media_player.set_media(media)

                if self.media_player.play() == -1:
                    QtCore.QMetaObject.invokeMethod(
                        self.ui.info_label,
                        "setText",
                        QtCore.Qt.ConnectionType.QueuedConnection,
                        QtCore.Q_ARG(str, "❌ Ошибка запуска"),
                    )
                    return

                self.is_playing = True
                station = self.ui.combo_list_radio.currentText()

                QtCore.QMetaObject.invokeMethod(
                    self.ui.info_label,
                    "setText",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(str, f"▶ Играет: {station}"),
                )
                QtCore.QMetaObject.invokeMethod(
                    self.ui.statusbar,
                    "showMessage",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(str, f"▶ {station}"),
                )

            except Exception as e:
                logger.error(f"Ошибка: {e}")
                self.is_playing = False

    def play_music(self):
        index = self.ui.combo_list_radio.currentIndex()
        if index < 0 or not self.radio_channels:
            return

        station = self.ui.combo_list_radio.currentText()
        url = self.radio_channels.get(station)

        if not url:
            logger.warning(f"URL не найден: {station}")
            return

        # Предупреждение если станция помечена как недоступная
        if self.station_status.get(station) is False:
            logger.warning(f"⚠️ Попытка запустить недоступную станцию: {station}")
            self.ui.info_label.setText(f"⚠️ {station} может быть недоступна")

        if self.is_playing:
            self._stop_current_stream()
        self._play_stream(url)

    def stop_music(self):
        with self._play_lock:
            self._stop_current_stream()
            self.ui.info_label.setText("⏹ Остановлено")
            self.ui.statusbar.showMessage("⏹ Остановлено")

    def on_channel_changed(self, index: int):
        """Обработчик смены станции в ComboBox."""
        # Опционально: автозапуск при смене канала
        if self.is_playing:
            station = self.ui.combo_list_radio.currentText()
            logger.info(f"Переключение на станцию: {station}")
            self.play_music()

    def set_volume(self, volume):
        if self.media_player and self.media_player.get_media():
            try:
                self.media_player.audio_set_volume(volume)
            except:
                pass

    def closeEvent(self, event):
        self.stop_music()
        QtCore.QThread.msleep(200)
        if self.media_player:
            self.media_player.release()
        if self.vlc_instance:
            self.vlc_instance.release()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Radio Player")

    window = MyWin()
    window.show()

    sys.exit(app.exec())
