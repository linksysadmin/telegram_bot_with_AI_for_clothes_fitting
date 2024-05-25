from aiogram import Router, F, html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown

from config import TELEGRAM_CHANEL_URL
import keyboards as kb
from filters.group_chat import IsNotSubscriber

router = Router(name=__name__)

MESSAGE_HELP = (f"📄 {markdown.hbold('Руководство:')}\n"
                f"Это бот для примерки одежды 🛍 \n"
                f"Для того, чтобы примерить одежду, вам потребуется загрузить изображения человека "
                f"и самой вещи.🩻\n\n"
                f"{markdown.hbold('Порядок действий следующий:')}\n\n"
                f"{markdown.hblockquote('1️⃣ Шаг: Выберите раздел и загрузите изображение человека.')}\n"
                f"{markdown.hblockquote('2️⃣ Шаг: Загрузите изображение одежды.')}\n"
                f"{markdown.hblockquote('3️⃣ Шаг: Ожидайте пока нейросеть сгенерирует изображение.')}\n(❗️Важно: Генерация изображения составляет около 20 секунд)\n\n"
                f"❌{html.bold('Заметка:')}\nИзображение должно четко выделять человека на общем фоне, с изображением одежды также.")

NOT_SUB_MESSAGE = f"Вам необходимо подписаться на наш канал ({TELEGRAM_CHANEL_URL}), чтобы использовать бота."


@router.message(Command(commands=['start', 'help']), IsNotSubscriber())
async def command_test_handler(message: Message) -> None:
    await message.answer(NOT_SUB_MESSAGE, reply_markup=await kb.subscribe())


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



@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(MESSAGE_HELP, reply_markup=await kb.clothing_types())
