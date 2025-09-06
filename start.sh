#!/bin/bash
# Запускаем Django и бота одновременно

# Запускаем Django в фоне
gunicorn tgsite.wsgi:application &

# Запускаем бота (останется в переднем плане)
python bot/bot.py
