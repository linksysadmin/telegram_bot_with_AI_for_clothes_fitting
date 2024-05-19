import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from telegram_app.handlers import router

# logging.basicConfig(stream=sys.stdout,
#                     level=logging.INFO,
#                     encoding='utf-8',
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     datefmt='%m.%d.%Y')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
