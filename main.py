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

from config import TELEGRAM_TOKEN, BASE_WEBHOOK_URL, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT, REDIS_URL
from app.middleware import UserMiddleware, ChatMemberHandlerMiddleware
from app.routers import router as main_router

logging.basicConfig(
    # stream=sys.stdout,
    filename='log.log',
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m.%d.%Y',
)

COMMANDS = [
    BotCommand(command='start', description='Начать'),
    BotCommand(command='help', description='Помощь'),
]

storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)
dp.message.outer_middleware.register(UserMiddleware(storage=storage))
dp.callback_query.outer_middleware.register(UserMiddleware(storage=storage))
dp.chat_member.outer_middleware.register(ChatMemberHandlerMiddleware(storage=storage))
dp.include_router(main_router)
# dp.message.middleware.register(LogMiddleware())
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# async def main() -> None:
#     try:
#         logging.basicConfig(level=logging.INFO)
#         await bot.set_my_commands(COMMANDS)
#         await dp.start_polling(bot)
#     except Exception as e:
#         logger.error(f"[EXCEPTION!!!] - {e}")
#     finally:
#         # await dp.storage.close()
#         await bot.session.close()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

async def on_startup(bot: Bot) -> None:
    await bot.set_my_commands(COMMANDS)
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        # secret_token=WEBHOOK_SECRET,
    )
    logging.warning(f'Вебхук задан: {await bot.get_webhook_info()}')



async def on_shutdown(bot):
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
        # secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    logging.info(f'Приложение запущено')
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


#
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)

