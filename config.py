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


# Replicate
# REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_MODEL = os.getenv("REPLICATE_MODEL", "cuuupid/idm-vton:906425dbca90663ff5427624839572cc56ea7d380343d13e2a4c4b09d3f0c30f")


# For WEBHOOK
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEB_SERVER_HOST = '0.0.0.0'  # прослушивать все доступные интерфейсы внутри контейнера Docker
WEB_SERVER_PORT = 8080  # прослушивать порт 8080 внутри контейнера Docker
WEBHOOK_PATH = f'/{TELEGRAM_TOKEN}/'

# Database and Redis
DATABASE = "sqlite+aiosqlite:///database.db"
REDIS_URL = 'redis://redis:6379/2'


DEBUG = os.getenv('DEBUG', False)
