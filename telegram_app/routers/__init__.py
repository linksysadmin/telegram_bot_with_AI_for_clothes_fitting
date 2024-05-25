__all__ = (
    "router",
)

from aiogram import Router

from .commands import router as commands_router
from .callbacks import router as callbacks_router
from .messages import router as messages_router
from telegram_app.middlewares import LogMiddleware

router = Router(name=__name__)
router.include_routers(
    commands_router,
    callbacks_router,
    messages_router,
)
router.message.middleware(LogMiddleware())
