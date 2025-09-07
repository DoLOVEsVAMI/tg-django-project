from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Бот работает через Webhook 🚀")

async def on_startup(app):
    webhook_url = "https://tg-django-project.onrender.com/webhook"
    await bot.set_webhook(webhook_url)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
setup_application(app, dp, bot=bot, on_startup=on_startup)

if __name__ == "__main__":
    web.run_app(app, port=10000)
