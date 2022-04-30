## Онлайн радио для дома.

![Radio](/img/Radio.png)

Для работы необходимы:
- Windows 10/11 x64 (x86)
- Win VLC Player x64 (x86)
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
git clone https://github.com/themasterid/Radio.git
```

Создаем виртуальное окружение venv:

```bash
python manage -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

Запускаем радио:

```bash
python Radio.pyw
```

Пользуемся.

## Сборка exe файла и сборка GUI PyQT5.

В терминале выполняем команды:

```bash
pyuic5 Radio_GUI.ui -o Radio_GUI.py
```

```bash
pyinstaller --onefile --noconsole --icon play.ico Radio.pyw
```
