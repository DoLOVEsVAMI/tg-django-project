from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

API_TOKEN = "7147939084:AAEg_yN3lj3tZZNEry5hFuL93e2oGEY6dD4"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Войти через Telegram",
                    web_app=types.WebAppInfo(
                        url="https://tg-django-project.onrender.com/accounts/telegram-login/"
                    )
                )
            ]
        ]
    )
    await message.answer("Привет! 👋 Нажми кнопку ниже для входа:", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
