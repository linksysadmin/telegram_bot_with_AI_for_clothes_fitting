from aiogram.filters import Filter
from aiogram.types import Message

from app.database.requests import db


class AvailableGeneration(Filter):
    async def __call__(self, message: Message) -> bool:
        user_data = await db.get_user_data(message.from_user.id)
        available_generation = user_data.get('available_generations')

        if available_generation:
            return True
        else:
            return False


