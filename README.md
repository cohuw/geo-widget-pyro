# ⛩ Shogun Pulse Widget

Минималистичный асинхронный скрипт для создания динамического виджета в Telegram-канале. Отображает текущее время и погоду в выбранных городах мира в реальном времени.

![Python](https://img.shields.io/badge/python-3.9+-blue?style=flat-square)
![Library](https://img.shields.io/badge/library-Pyrogram-orange?style=flat-square)

## 📋 Особенности
- **Async Architecture:** Параллельный сбор данных через `aiohttp` и `asyncio.gather`.
- **Solar-Sync:** Динамические иконки (✨, 🌅, ☀️, 🌇, 🌙), меняющиеся в зависимости от времени суток в конкретном часовом поясе.
- **Weather Integration:** Актуальная температура и погодные условия через Open-Meteo API (без ключей).
- **Clean UI:** Оформление в стиле терминального вывода с использованием моноширинных шрифтов.

## 🚀 Быстрый старт

1. **Установи зависимости:**
```bash
pip install -r requirements.txt
```


2. Настрой конфигурацию:
Открой файл и заполни следующие поля в секции CONFIG:
* API_ID / API_HASH — получи на [my.telegram.org](https://my.telegram.org).
* BOT_TOKEN — от @BotFather.
* CHAT_ID — ID канала или чата, где будет виджет.
* LOG_MESSAGE_ID — ID заранее созданного сообщения, которое бот будет редактировать.


3. Запусти:
```bash
python widget.py
```


## ⚙️ Технологии

* Kurigram (Fork of Pyrogram): Для работы с Telegram API.
* Aiohttp: Для быстрых асинхронных HTTP-запросов.
* Pytz: Для точной работы с часовыми поясами.
* Open-Meteo: В качестве источника данных о погоде.