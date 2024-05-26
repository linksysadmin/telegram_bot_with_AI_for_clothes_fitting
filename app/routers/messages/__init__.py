__all__ = (
    "router",
)

from aiogram import Router

from .media_handlers import router as user_messages_router

router = Router(name=__name__)

router.include_router(user_messages_router)
