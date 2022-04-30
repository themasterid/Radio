## Онлайн радио для дома.

![Radio](/img/Radio.png)

Для работы необходимы:
- Windows 10/11 x64 или Ubuntu 22.04 x64
- Win VLC Player x64 или Linux VLC Player
- python-vlc
- PyQt5
- pyinstaller

Если возникнут проблемы при создании exe файла:
```bash
pip uninstall -y enum34
```

## Установка

Клонируем репозиторий на ПК:

```bash
git clone git@github.com:themasterid/Radio.git
or
git clone https://github.com/themasterid/Radio.git
```

Создаем виртуальное окружение venv:

- Windows
```bash
python -m venv venv
```
- Linux
```bash
python3 -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

Устанавливаем зависимости:

- Windows
```bash
pip install -r requirements.txt
```

- Linux
```bash
sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

Запускаем радио:

- Windows
```bash
python Radio.pyw
```

- Linux
```bash
python3 Radio.pyw
```

Пользуемся.

## Сборка exe файла и сборка GUI PyQT5 в Windows.

В терминале выполняем команды:

```bash
pyuic5 Radio_GUI.ui -o Radio_GUI.py
```

```bash
pyinstaller --onefile --noconsole --icon play.ico Radio.pyw
```
