from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import keyboards as kb
from app.database.requests import db
from app.templates.messages_templates import MESSAGE_HELP

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/start', для отправки приветственного сообщения.
    Добавляет пользователя в БД, в случае его отсутствия.
    :param message: Сообщение-entity
    :param state: Состояние
    """
    user_id = message.from_user.id
    check_user = await db.get_user_data(user_id=user_id)
    if not check_user:
        await db.add_user(user_id=user_id)
    await state.clear()
    await message.answer(f"Здравствуйте!, {html.bold(message.from_user.full_name)}!\n"
                         f"Вас приветствует бот для примерки.\n\n"
                         + MESSAGE_HELP,
                         reply_markup=await kb.clothing_types())


@router.message(Command('help'))
async def command_test_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/help', для отправки инструктирующего сообщения.
    :param message: Сообщение-entity
    :param state: Состояние
    """
    await state.clear()
    await message.answer(text=MESSAGE_HELP, reply_markup=await kb.clothing_types())


@router.message(Command('buy'))
async def command_buy_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/buy', для покупки генераций.
    :param message: Сообщение-entity
    :param state: Состояние
    """
    await state.clear()
    await message.answer(f'Выберите количество генераций, которые вы хотите приобрести:\n\n'
                         f'💛15 - 179 руб.\n'
                         f'🩵30 - 279 руб.\n'
                         f'❤️50 - 379 руб.\n',
                         reply_markup=await kb.generations())


@router.message(Command('profile'))
async def command_buy_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/profile'
    :param message: Сообщение-entity
    :param state: Состояние
    """
    await state.clear()

    user_id = message.from_user.id
    user_data = await db.get_user_data(user_id)
    if user_data:
        await message.answer(f'Личный кабинет:\n\n'
                             f'Имя: {message.from_user.first_name}\n'
                             f'ID: {user_id}\n'
                             f'Доступно генераций: {user_data["available_generations"]}\n'
                             f'Использовано генераций: {user_data["used_generations"]}\n\n'
                             f'Купить генерации: /buy\n'
                             f'Нажмите /start для генерации изображения'
                             )
    else:
        await message.answer(f'Нажмите /start для начала')
