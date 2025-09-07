from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хэндлер для команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(
            text="Открыть приложение 🚀",
            web_app=types.WebAppInfo(
                url="https://tg-django-project.onrender.com/accounts/telegram-login/"
            )
        )]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Привет! Жми кнопку ниже, чтобы войти через сайт 👇", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
