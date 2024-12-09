@echo off
echo Installing dependencies...

REM Проверка наличия pip
python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip не установлен. Устанавливаю pip...
    python -m ensurepip --upgrade
)

REM Установка virtualenv, если требуется
IF NOT EXIST venv (
    echo Создание виртуального окружения...
    python -m venv venv
)

REM Активация виртуального окружения
call venv\Scripts\activate

REM Установка зависимостей из requirements.txt
pip install --upgrade pip
IF EXIST requirements.txt (
    echo Установка зависимостей из requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt не найден, установка стандартных зависимостей...
    pip install telethon yt-dlp python-dotenv cryptg
)

echo Зависимости успешно установлены!
pause
