import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
TELEGRAM_CHANEL_ID = os.getenv("TELEGRAM_CHANEL_ID")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# Replicate
# REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# For WEBHOOK
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
WEBHOOK_PATH = f'/{TELEGRAM_TOKEN}'
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))
