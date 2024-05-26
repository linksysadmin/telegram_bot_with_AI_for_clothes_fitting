import logging
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, TelegramObject, ChatMemberLeft, CallbackQuery, ChatMember
from aiogram.fsm.storage.redis import RedisStorage

from app.keyboards import subscribe
from app.messages_templates import NOT_SUB_MESSAGE
from config import TELEGRAM_CHANEL_ID


# class LogMiddleware(BaseMiddleware):
#
#     async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
#         result = await handler(event, data)
#         return result


class UserMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:

        user = f'user_{event.from_user.id}'
        logging.info(f"MIDDLEWARE:{self.__class__.__name__}: key: {user}")

        check_user = await self.storage.redis.get(name=user)
        if check_user:
            return await handler(event, data)
        else:
            user_status = await event.bot.get_chat_member(chat_id=TELEGRAM_CHANEL_ID, user_id=event.from_user.id)
            match user_status:
                case ChatMemberLeft():
                    if type(event) == CallbackQuery:
                        return await event.message.edit_text(NOT_SUB_MESSAGE, reply_markup=await subscribe())
                    return await event.answer(NOT_SUB_MESSAGE, reply_markup=await subscribe())
                case _:
                    await self.storage.redis.set(name=user, value=1)
                    return await handler(event, data)


class ChatMemberHandlerMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[ChatMember, Dict[str, Any]], Awaitable[Any]],
                       event: ChatMember,
                       data: Dict[str, Any]) -> Any:
        user = f'user_{event.from_user.id}'
        logging.info(f"MIDDLEWARE:{self.__class__.__name__}: key: {user}")

        match event.new_chat_member.status:
            case ChatMemberStatus.MEMBER:
                await self.storage.redis.set(name=user, value=1)
            case ChatMemberStatus.LEFT:
                await self.storage.redis.delete(user)

        return await handler(event, data)



        # check_user = await self.storage.redis.get(name=user)
        # if check_user:
        #     return await handler(event, data)
        # else:
        #     user_status = await event.bot.get_chat_member(chat_id=TELEGRAM_CHANEL_ID, user_id=event.from_user.id)
        #     if isinstance(user_status, ChatMemberLeft):
        #         return await event.answer(NOT_SUB_MESSAGE, reply_markup=await subscribe())
        #     else:
        #         await self.storage.redis.set(name=user, value=1)
        #         return await handler(event, data)
        #





# class RedisMiddleware(BaseMiddleware):
#     def __init__(self, storage: RedisStorage):
#         self.storage = storage
#
#     async def __call__(self,
#                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#                        event: Message,
#                        data: Dict[str, Any]) -> Any:
#
#         user = f'user_{event.from_user.id}'
#         check_user = await self.storage.redis.get(name=user)
#         if check_user:
#             if int(check_user.decode()) == 1:
#                 await self.storage.redis.set(name=user, value=0, ex=10)
#                 return await event.answer('Ждите 10 секунд...')
#             return
#         await self.storage.redis.set(name=user, value=1, ex=10)
#         return await handler(event, data)

