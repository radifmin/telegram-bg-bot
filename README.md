# Telegram Background Replacement Bot

Бот для удаления и замены фона на изображениях (тестовое задание для SearchBooster)

Протестировать бота можно на t.me/radifmin_searchboosterbot

## Установка и запуск

### Локальный запуск
1. Клонировать репозиторий:
```bash
git clone https://github.com/radifmin/telegram-bg-bot.git
cd telegram-bg-bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создать файл `.env`:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
BACKGROUND_IMAGE=path/to/image.jpg # путь до файла с фоном
```

4. Запустить бота:
```bash
python bot.py
```
