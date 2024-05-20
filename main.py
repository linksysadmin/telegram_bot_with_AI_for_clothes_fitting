import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import TOKEN
from telegram_app.handlers import router

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m.%d.%Y')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
COMMANDS = [
    BotCommand(command='start', description='Начать'),
    BotCommand(command='cancel', description='Отменить'),
    BotCommand(command='help', description='Помощь'),
]



async def main() -> None:
    dp.include_router(router)
    await bot.set_my_commands(COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
