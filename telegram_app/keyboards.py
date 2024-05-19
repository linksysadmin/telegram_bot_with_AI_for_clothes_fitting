from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def start():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отправить фото', callback_data='send_photo'))
    return keyboard.as_markup()


async def exit():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    return keyboard.as_markup()






