from aiogram import Bot, Dispatcher, types
import asyncio

bot = Bot("7147939084:AAEg_yN3lj3tZZNEry5hFuL93e2oGEY6dD4")
dp = Dispatcher()

@dp.message(commands=["start"])
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Открыть приложение",
                web_app=types.WebAppInfo(url="https://tg-django-project.onrender.com/accounts/telegram-login/")
            )]
        ]
    )
    await message.answer("Запусти мини-апп 👇", reply_markup=kb)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
