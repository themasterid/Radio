## Онлайн Радио для дома.

# TODO Переписать на PyQT6 c выводом названия треков и прочей мути...

![Radio](/img/Radio.png)

Стек для работы:
- Debian 12 x64
- Linux VLC Player
- python-vlc
- PyQt5

## Клонируем и устанавливаем UV и виртуальное окружение:

Клонируем репозиторий:

```bash
git clone git@github.com:themasterid/Radio.git
```

или

```bash
git clone https://github.com/themasterid/Radio.git
```

Создаем виртуальное окружение через UV с его установкой:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Активируем виртуальное окружение:

```bash
uv venv
```

Устанавливаем зависимости из файла requirements.txt:

```bash
uv pip install -r requirements.txt
```

Запускаем Радио и слушаем:

```bash
python3 Radio.pyw
```

Если вдруг вам нужно все это дело запустить в Windows или собрать exe:

## Сборка exe файла и сборка GUI PyQT5 в Windows.

В терминале выполняем команды:

```bash
pyuic5 Radio_GUI.ui -o Radio_GUI.py
```

```bash
pyinstaller --onefile --noconsole --icon play.ico Radio.pyw
```

Автор: [Дмитрий Клепиков](https://github.com/themasterid) :+1: