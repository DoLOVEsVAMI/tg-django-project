from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot("7147939084:AAEg_yN3lj3tZZNEry5hFuL93e2oGEY6dD4")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "Открыть приложение",
        web_app=types.WebAppInfo(url="http://127.0.0.1:8000/accounts/telegram-login/")
    ))
    await message.answer("Запусти мини-апп 👇", reply_markup=kb)

executor.start_polling(dp, skip_updates=True)
