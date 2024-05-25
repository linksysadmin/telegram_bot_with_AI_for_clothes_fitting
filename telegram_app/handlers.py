import logging
import io

import aiohttp
from aiogram import Router, F, html, types
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from aiogram.utils.chat_action import ChatActionSender

import telegram_app.keyboards as kb
from telegram_app.filters.group_chat import IsSubscriber
from telegram_app.states import Photo
from telegram_app.middlewares import LogMiddleware
from image_handler import get_url_converted_image

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(LogMiddleware())

MESSAGE_HELP = (f"📄 {markdown.hbold('Руководство:')}\n"
                f"Это бот для примерки одежды 🛍 \n"
                f"Для того, чтобы примерить одежду, вам потребуется загрузить изображения человека "
                f"и самой вещи.🩻\n\n"
                f"{markdown.hbold('Порядок действий следующий:')}\n\n"
                f"{markdown.hblockquote('1️⃣ Шаг: Выберите раздел и загрузите изображение человека.')}\n"
                f"{markdown.hblockquote('2️⃣ Шаг: Загрузите изображение одежды.')}\n"
                f"{markdown.hblockquote('3️⃣ Шаг: Ожидайте пока нейросеть сгенерирует изображение.')}\n(❗️Важно: Генерация изображения составляет около 20 секунд)\n\n"
                f"❌{html.bold('Заметка:')}\nИзображение должно четко выделять человека на общем фоне, с изображением одежды также.")

NOT_SUB_MESSAGE = "Для доступа к боту вам необходимо подписаться на канал!"


@router.message(CommandStart(), IsSubscriber())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здравствуйте!, {html.bold(message.from_user.full_name)}!\n"
                         f"Вас приветствует бот для примерки.\n\n"
                         + MESSAGE_HELP,
                         reply_markup=await kb.clothing_types())


@router.message(Command('help'))
async def command_test_handler(message: Message) -> None:
    await message.answer(text=MESSAGE_HELP, reply_markup=await kb.clothing_types())


@router.callback_query(kb.ClothTypeCallbackData.filter())
async def handler_type_cloth_callback(callback: CallbackQuery, callback_data: kb.ClothTypeCallbackData,
                                      state: FSMContext):
    await state.update_data(cloth=callback_data.cloth)
    await state.set_state(Photo.human_img)
    await callback.answer('1️⃣ Загрузите изображение человека')
    for cloth_type in kb.cloth_types:
        if cloth_type.api_string == callback_data.cloth:
            await callback.message.edit_text(f'Категория:\n{html.bold(cloth_type.description)}\n\n'
                                             f'1️⃣ Загрузите изображение человека', reply_markup=await kb.cancel())


@router.message(Photo.human_img, F.photo)
async def get_human_img(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    human_img = io.BytesIO()

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    await message.bot.download(file=file_id, destination=human_img)
    await state.update_data(human_img=human_img)
    user_data = await state.get_data()
    await state.set_state(Photo.garm_img)
    for cloth_type in kb.cloth_types:
        if cloth_type.api_string == user_data['cloth']:
            await message.answer(f'Категория:\n{html.bold(cloth_type.description)}\n\n'
                                 f'2️⃣ Шаг: Загрузите изображение одежды', reply_markup=await kb.cancel())


@router.message(Photo.garm_img, F.photo)
async def get_garm_img(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    garm_img = io.BytesIO()

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    await message.bot.download(file=file_id, destination=garm_img)
    await state.update_data(garm_img=garm_img)
    await send_image(message, state)
    user_data = await state.get_data()
    for cloth_type in kb.cloth_types:
        if cloth_type.api_string == user_data['cloth']:
            await message.answer(f'Категория:\n{html.bold(cloth_type.description)}\n\n'
                                 f'1️⃣ Загрузите изображение человека', reply_markup=await kb.cancel())
    await state.set_state(Photo.human_img)


async def send_image(message, state):
    await message.answer(text=f'Подождите немного...\nБот старается вас одеть 😊\n\n'
                              f'❗️Важно: Генерация изображения составляет около 20 секунд')
    await message.answer_dice(emoji='🎲')

    user_data = await state.get_data()
    logger.info(f"Данные пользователя при отправке фото: {user_data}")

    data_images = {
        "human_img": user_data['human_img'],
        "garm_img": user_data['garm_img'],
        "garment_des": "cute",
        "category": user_data['cloth'],
    }

    async with ChatActionSender.upload_photo(
            bot=message.bot,
            chat_id=message.chat.id,
    ):
        image_url = await get_url_converted_image(data_images)
        if image_url:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    result_bytes = await response.read()
            await message.reply_document(
                document=types.BufferedInputFile(
                    file=result_bytes,
                    filename='Результат.jpeg'
                )
            )
            logger.info("Удачная отправка изображения пользователю")
        else:
            await message.answer(text=f'К сожалению боту не удалось распознать ваши изображения.\n'
                                      f'Загрузите изображения,  на которых четко выделяются как человек, так и одежда.')


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(MESSAGE_HELP, reply_markup=await kb.clothing_types())


@router.message(Photo.human_img, F.text)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение,  на котором четко выделяется человек',
                         reply_markup=await kb.cancel())


@router.message(Photo.garm_img, F.text)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение, на котором четко выделяется одежда',
                         reply_markup=await kb.cancel())
