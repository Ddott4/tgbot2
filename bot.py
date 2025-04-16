import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# ==== НАСТРОЙКИ ====
BOT_TOKEN = "8195781148:AAFc9b8CxrX8a9JYEQvN_hUAyjCNflVC5L8"                  # Вставьте токен
CHANNEL_USERNAME = "@GoCrypto10"       # Название канала
ADMIN_ID = 1580610086                     # Ваш Telegram ID

# ==== ИНИЦИАЛИЗАЦИЯ ====
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ==== БАЗА ДАННЫХ SQLite ====
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]

# ==== КНОПКА ====
check_sub_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_sub")]
])

# ==== ПРОВЕРКА ПОДПИСКИ ====
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# ==== /start ====
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    add_user(user_id)

    if await is_subscribed(user_id):
        await message.answer("✅ Вы подписаны! Вот ваша ссылка:\nhttps://teletype.in/@coinstart/bszS77gLhb")
    else:
        await message.answer(
            f"❗ Чтобы получить доступ, подпишитесь на {CHANNEL_USERNAME} и нажмите кнопку ниже:",
            reply_markup=check_sub_button
        )

# ==== ОБРАБОТКА КНОПКИ ====
@dp.callback_query(F.data == "check_sub")
async def handle_check_sub(callback: CallbackQuery):
    user_id = callback.from_user.id

    if await is_subscribed(user_id):
        await callback.message.edit_text("✅ Подписка подтверждена!\nВот ваша ссылка: https://teletype.in/@coinstart/bszS77gLhb")
    else:
        await callback.answer("❌ Вы ещё не подписались", show_alert=True)

# ==== /broadcast ====
@dp.message(Command("broadcast"))
async def broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("❗ Введите сообщение после команды:\nНапример: /broadcast Привет всем!")
        return

    users = get_all_users()
    sent = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except:
            continue

    await message.answer(f"✅ Отправлено {sent} пользователям.")

# ==== ЗАПУСК ====
async def main():
    print("✅ Бот запускается...")
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 Бот запущен и ждёт команды!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

