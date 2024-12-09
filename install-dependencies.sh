#!/bin/bash
echo "Installing dependencies..."

# Проверка наличия Python и pip
if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Установите Python3 и повторите попытку."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip не установлен. Устанавливаю pip..."
    python3 -m ensurepip --upgrade
    python3 -m pip install --upgrade pip
fi

# Создание виртуального окружения, если его нет
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей из requirements.txt
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    echo "Установка зависимостей из requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt не найден, установка стандартных зависимостей..."
    pip install telethon yt-dlp python-dotenv cryptg
fi

echo "Зависимости успешно установлены!"
