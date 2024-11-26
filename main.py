import asyncio
import logging
import os
import sys

from aiohttp import web

from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


from config import TELEGRAM_TOKEN, WEBHOOK_URL, WEB_SERVER_HOST, WEB_SERVER_PORT, REDIS_URL, DEBUG
from app.middleware.base_middlewares import ChannelHandlerMiddleware
from app.middleware.user_middleware import CheckUserInGroupMiddleware
from app.routers import router as main_router

logging.basicConfig(
    stream=sys.stdout,
    # filename='log.log',
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m.%d.%Y',
)



storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher()
# dp.message.outer_middleware.register(CheckUserInGroupMiddleware(storage=storage))
# dp.callback_query.outer_middleware.register(CheckUserInGroupMiddleware(storage=storage))
dp.chat_member.outer_middleware.register(ChannelHandlerMiddleware(storage=storage))
dp.include_router(main_router)
# dp.message.middleware.register(LogMiddleware())
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

COMMANDS = [
    BotCommand(command='start', description='Начать'),
    BotCommand(command='help', description='Помощь'),
    BotCommand(command='buy', description='Купить генерации'),
    BotCommand(command='profile', description='Личный кабинет'),
]



async def on_startup(bot: Bot) -> None:
    await bot.set_my_commands(COMMANDS)
    await bot.set_webhook(WEBHOOK_URL)
    logging.warning(f'Вебхук задан: {await bot.get_webhook_info()}')


async def on_shutdown(bot):
    await storage.redis.flushdb()
    logging.warning(f'Redis очищен')
    await bot.delete_webhook()
    logging.warning(f'Вебхук удален')


def main() -> None:
    # При запуске приложения
    dp.startup.register(on_startup)

    # При закрытии приложения
    dp.shutdown.register(on_shutdown)
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(  # TokenBasedRequestHandler
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=f'')
    setup_application(app, dp, bot=bot)

    logging.info(f'Приложение запущено')
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


async def start_bot_testing_mode() -> None:
    try:
        await dp.start_polling(bot)
    finally:
        await storage.redis.flushdb()
        await bot.session.close()


if __name__ == "__main__":
    if DEBUG:
        asyncio.run(start_bot_testing_mode())
    else:
        main()

