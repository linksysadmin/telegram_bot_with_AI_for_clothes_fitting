import io
import logging

import aiohttp
from aiogram import Router, F, types, html
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender


from app.image_handler import get_url_converted_image
from app import keyboards as kb
from app.states import Photo

logger = logging.getLogger(__name__)

router = Router(name=__name__)


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


@router.message(Photo.human_img, F.text)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение,  на котором четко выделяется человек',
                         reply_markup=await kb.cancel())


@router.message(Photo.garm_img, F.text)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение, на котором четко выделяется одежда',
                         reply_markup=await kb.cancel())
