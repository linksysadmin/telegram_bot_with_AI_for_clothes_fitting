import os

from aiogram.types import BotCommand
from dotenv import load_dotenv

load_dotenv()

# Database and Redis
DATABASE = "sqlite+aiosqlite:///database.db"
REDIS_URL = os.getenv("REDIS_URL")

# Telegram Bot
TELEGRAM_CHANEL_ID = os.getenv("TELEGRAM_CHANEL_ID")
TELEGRAM_CHANEL_URL = os.getenv("TELEGRAM_CHANEL_URL")  # https://t.me/+08LyQf5vkQUyNzli
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
COMMANDS = [
    BotCommand(command='start', description='Начать'),
    BotCommand(command='help', description='Помощь'),
]

# Replicate
# REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_MODEL = os.getenv("REPLICATE_MODEL", "cuuupid/idm-vton:906425dbca90663ff5427624839572cc56ea7d380343d13e2a4c4b09d3f0c30f")

# For WEBHOOK
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
WEBHOOK_PATH = f'/{TELEGRAM_TOKEN}'
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))

DEBUG = os.getenv('DEBUG', True)
