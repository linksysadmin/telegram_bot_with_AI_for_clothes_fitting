from aiogram.filters import Filter
from aiogram.types import Message, ChatMemberLeft

from config import TELEGRAM_CHANEL_ID


class IsSubscriber(Filter):
    async def __call__(self, message: Message) -> bool:
        user_status = await message.bot.get_chat_member(chat_id=TELEGRAM_CHANEL_ID, user_id=message.from_user.id)
        if isinstance(user_status, ChatMemberLeft):
            return False
        else:
            return True


