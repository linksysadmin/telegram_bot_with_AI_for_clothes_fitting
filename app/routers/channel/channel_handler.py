import logging
from typing import Any

from aiogram import Router, html, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import keyboards as kb
from app.messages_templates import MESSAGE_HELP

router = Router(name=__name__)


# @router.chat_join_request()
# async def chat_join_request_handler(chat_join_request: types.ChatJoinRequest) -> Any:
#     logging.info(f"chat_join_request: {chat_join_request}")


@router.chat_member()
async def chat_member(chat_member: types.ChatMemberUpdated) -> Any: pass


