@echo off
echo Starting yuki-bot...

REM Проверка наличия виртуального окружения
IF NOT EXIST venv (
    echo Виртуальное окружение не найдено. Убедитесь, что зависимости установлены.
    pause
    exit /b
)

REM Активация виртуального окружения
call venv\Scripts\activate.bat

REM Запуск скрипта бота
python bot.py

REM Деактивация виртуального окружения после завершения работы
deactivate
echo Бот остановлен.
pause
