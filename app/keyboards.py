from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TELEGRAM_CHANEL_URL


class ClothType(Enum):
    upper_body = 'Примерка топа'
    lower_body = 'Примерка низа'
    dresses = 'Примерка платья'


class ClothTypeCallbackData(CallbackData, prefix="cloth"):
    cloth: str


class GenerationAmountCallbackData(CallbackData, prefix="gen_amount"):
    gen_amount: int
    price: float


PRICE_FOR_GENERATIONS = {
    15: 179,
    30: 279,
    50: 379,
}


async def clothing_types():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=ClothType.upper_body.value, callback_data=ClothTypeCallbackData(cloth=ClothType.upper_body.name).pack())
    keyboard.button(text=ClothType.lower_body.value, callback_data=ClothTypeCallbackData(cloth=ClothType.lower_body.name).pack())
    keyboard.button(text=ClothType.dresses.value, callback_data=ClothTypeCallbackData(cloth=ClothType.dresses.name).pack())
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


async def generations():
    keyboard = InlineKeyboardBuilder()
    for gen, price in PRICE_FOR_GENERATIONS.items():
        keyboard.button(text=str(gen), callback_data=GenerationAmountCallbackData(gen_amount=gen, price=price).pack())
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    keyboard.adjust(2)
    return keyboard.as_markup()
