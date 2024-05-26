from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import keyboards as kb
from app.messages_templates import MESSAGE_HELP

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Здравствуйте!, {html.bold(message.from_user.full_name)}!\n"
                         f"Вас приветствует бот для примерки.\n\n"
                         + MESSAGE_HELP,
                         reply_markup=await kb.clothing_types())


@router.message(Command('help'))
async def command_test_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=MESSAGE_HELP, reply_markup=await kb.clothing_types())
