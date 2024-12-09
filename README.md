# 🌸 Yuki Bot

> **Бот для скачивания видео с YouTube в высоком качестве.**  
> Простой запуск, удобная настройка и гибкие возможности.

## 📦 Быстрый старт

1. **Установите зависимости**  
   Запустите один из скриптов:

   - **Windows**: `install-dependencies.bat`
   - **Linux/MacOS**: `install-dependencies.sh`

2. **Создайте файл `.env`**  
   Пример:

   ```env
   API_ID=12345678
   API_HASH=12345678901234567890123456789012
   ALLOWED_IDS=123456789 # Укажите ID пользователей или * для всех

   ```

3. **Запустите бота**
   - Windows: `run-bot.bat`
   - Linux/MacOS: `run-bot.sh`

## 📜 Альтернативная настройка

Если предпочитаете настроить вручную:

### 🗃️ Виртуальное окружение

**Windows**:

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/MacOS**:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 📃 Установка зависимостей

**Windows**:

```cmd
pip install -r requirements.txt
```

**Linux/MacOS**:

```bash
pip3 install -r requirements.txt
```

### 🚀 Запуск

**Windows**:

```cmd
python bot.py
```

**Linux/MacOS**:

```bash
python3 bot.py
```

## 🌟 Особенности

- Удобная настройка: все конфигурации через `.env`
- Кроссплатформенность: поддержка Windows, Linux, и MacOS.
- Простое развертывание: скрипты автоматизируют установку и запуск.

## 🛠️ Требования

- Python 3.10+
- Установленные зависимости из `requirements.txt`

## 💌 Поддержка

Если возникли вопросы или предложения, создайте `issue` или свяжитесь со мной.
