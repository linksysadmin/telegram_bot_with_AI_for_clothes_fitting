from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TypeClothCbData(CallbackData, prefix="photo"):
    cloth: str


CATEGORIES = {
    "upper_body": "Примерка топа",
    "lower_body": "Примерка низа",
    "dresses": "Примерка платья",
}


async def start():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=CATEGORIES["upper_body"], callback_data=TypeClothCbData(cloth="upper_body").pack())
    keyboard.button(text=CATEGORIES["lower_body"], callback_data=TypeClothCbData(cloth="lower_body").pack())
    keyboard.button(text=CATEGORIES["dresses"], callback_data=TypeClothCbData(cloth="dresses").pack())
    keyboard.adjust(1)
    return keyboard.as_markup()


async def exit():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='exit'))
    return keyboard.as_markup()






