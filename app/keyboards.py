from typing import Iterator

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TELEGRAM_CHANEL_URL


class ClothType:
    def __init__(self, api_string: str, description: str):
        self.api_string = api_string
        self.description = description


class ClothTypesList:
    def __init__(self):
        self._cloth_types = []

    def add_type(self, cloth_type: ClothType):
        self._cloth_types.append(cloth_type)

    def __iter__(self) -> Iterator[ClothType]:
        return iter(self._cloth_types)


class ClothTypeCallbackData(CallbackData, prefix="cloth"):
    cloth: str


cloth_types = ClothTypesList()
cloth_types.add_type(ClothType("upper_body", "Примерка топа"))
cloth_types.add_type(ClothType("lower_body", "Примерка низа"))
cloth_types.add_type(ClothType("dresses", "Примерка платья"))


async def clothing_types():
    keyboard = InlineKeyboardBuilder()
    for c_type in cloth_types:
        keyboard.button(text=c_type.description, callback_data=ClothTypeCallbackData(cloth=c_type.api_string).pack())
    keyboard.adjust(1)
    return keyboard.as_markup()


async def cancel():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    return keyboard.as_markup()


async def subscribe():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='✅Подписаться', url=TELEGRAM_CHANEL_URL))
    return keyboard.as_markup()


