import logging
import io

import aiohttp
from aiogram import Router, F, html, types
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.utils.chat_action import ChatActionSender

import telegram_app.keyboards as kb
from telegram_app.states import Photo
from telegram_app.middlewares import LogMiddleware
from image_procissing import get_url_converted_image

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(LogMiddleware())

START_MESSAGE = (f"📄 {html.bold('Руководство:')}\n\n"
                 f"Это бот для примерки одежды 🌠\n\n"
                 f"🎉🛍 Для того, чтобы примерить одежду, вам потребуется загрузить изображения человека "
                 f"и самой вещи.🩻\n\n"
                 f"{html.bold('Порядок действий следующий:')}\n\n"
                 f"Для начала вам нужно нажать /start.\n"
                 f"1️⃣ Шаг: Выберите раздел и загрузите изображение человека.\n"
                 f"2️⃣ Шаг: Загрузите изображение одежды.\n"
                 f"3️⃣ Шаг: Ожидайте пока нейросеть сгенерирует изображение.\n(❗️Важно: Генерация изображения составляет около 20 секунд)\n\n"
                 f"❌❗️{html.bold('Заметка:')}\nИзображение должно четко выделять человека на общем фоне, с изображением одежды также.")


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здравствуйте!, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Вас приветствует бот для примерки.\n\n"
                         + START_MESSAGE,
                         reply_markup=await kb.start())


# @router.message(Command('test'))
# async def command_test_handler(message: Message) -> None:
#
#     TEST = {
#         "garm_img": "https://replicate.delivery/pbxt/KgwTlZyFx5aUU3gc5gMiKuD5nNPTgliMlLUWx160G4z99YjO/sweater.webp",
#         "human_img": "https://replicate.delivery/pbxt/KgwTlhCMvDagRrcVzZJbuozNJ8esPqiNAIJS3eMgHrYuHmW4/KakaoTalk_Photo_2024-04-04-21-44-45.png",
#         "garment_des": "cute pink top"
#     }
#
#     await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
#     image_url = await get_url_converted_image(TEST)
#     await message.reply_photo(photo=image_url, caption='Преобразованное фото')


@router.message(Command('help'))
async def command_test_handler(message: Message) -> None:
    await message.answer(text=START_MESSAGE)


@router.callback_query(kb.TypeClothCbData.filter())
async def handler_type_cloth_callback(callback: CallbackQuery, callback_data: kb.TypeClothCbData, state: FSMContext):
    await state.update_data(cloth=callback_data.cloth)
    await state.set_state(Photo.human_img)
    await callback.answer('1️⃣ Загрузите изображение человека')
    await callback.message.answer(f'Вы находитесь в категории:\n{html.bold(kb.CATEGORIES[callback_data.cloth])}\n\n1️⃣ Загрузите изображение человека', reply_markup=await kb.exit())


@router.message(Photo.human_img, F.photo)
async def get_human_img(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    human_img = io.BytesIO()

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    await message.bot.download(file=file_id, destination=human_img)
    await state.update_data(human_img=human_img)
    user_data = await state.get_data()
    await state.set_state(Photo.garm_img)
    await message.answer(text=f'Вы находитесь в категории:\n{html.bold(kb.CATEGORIES[user_data["cloth"]])}\n\n2️⃣ Шаг: Загрузите изображение одежды', reply_markup=await kb.exit())


@router.message(Photo.garm_img, F.photo)
async def get_garm_img(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    garm_img = io.BytesIO()

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    await message.bot.download(file=file_id, destination=garm_img)
    await state.update_data(garm_img=garm_img)
    await send_image(message, state)
    user_data = await state.get_data()
    await message.answer(f'Вы находитесь в категории:\n{html.bold(kb.CATEGORIES[user_data["cloth"]])}\n\n1️⃣ Загрузите изображение человека', reply_markup=await kb.exit())
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

    # async with ChatActionSender.upload_photo(
    #         bot=message.bot,
    #         chat_id=message.chat.id,
    # ):
    #     image_url = await get_url_converted_image(data_images)
    #     if image_url:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(image_url) as response:
    #                 result_bytes = await response.read()
    #         await message.reply_document(
    #             document=types.BufferedInputFile(
    #                 file=result_bytes,
    #                 filename='Результат.jpeg'
    #             )
    #         )
    #     else:
    #         await message.answer(text=f'К сожалению боту не удалось распознать ваши изображения.\n'
    #                                   f'Загрузите изображения,  на которых четко выделяются как человек, так и одежда.')


@router.callback_query(F.data == 'exit')
async def exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(f"Бот для примерки.\nНажмите 'Отправить фото' и загрузите ваше изображения",
                                     reply_markup=await kb.start())


@router.message(Photo.human_img, F.text)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение,  на котором четко выделяется человек', reply_markup=await kb.exit())


@router.message(Photo.garm_img, F.text)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение, на котором четко выделяется одежда', reply_markup=await kb.exit())

