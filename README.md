# Telegram Bot для Render.com

Этот бот:
- Проверяет подписку на канал
- Выдаёт ссылку только подписанным
- Сохраняет всех пользователей в SQLite
- Позволяет администратору делать рассылки

## 🔧 Запуск на Render

1. Залей проект на GitHub
2. Перейди на [https://render.com](https://render.com)
3. Создай Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
4. Добавь переменные окружения:
   - `BOT_TOKEN=ваш_токен`

👉 Бот запустится автоматически.
