import logging
import io

import aiohttp
from aiogram import Router, F, html, types
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender

import telegram_app.keyboards as kb
from telegram_app.states import Photo
from telegram_app.middlewares import LogMiddleware
from image_procissing import get_url_converted_image


logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(LogMiddleware())


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здравствуйте!, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Вас приветствует бот для примерки.\nНажмите 'Отправить фото' и загрузите ваше изображения",
                         reply_markup=await kb.start())


@router.message(Command('test'))
async def command_test_handler(message: Message) -> None:
    # data = await data_images(1, 2)
    # result_1 = await get_converted_image(data)
    # async def data_images():
    #     test = {
    #         "garm_img": "https://replicate.delivery/pbxt/KgwTlZyFx5aUU3gc5gMiKuD5nNPTgliMlLUWx160G4z99YjO/sweater.webp",
    #         "human_img": "https://replicate.delivery/pbxt/KgwTlhCMvDagRrcVzZJbuozNJ8esPqiNAIJS3eMgHrYuHmW4/KakaoTalk_Photo_2024-04-04-21-44-45.png",
    #         "garment_des": "cute pink top"
    #     }
    #     return test
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    image_url = await get_url_converted_image({})
    await message.reply_photo(photo=image_url,
                              caption='преобразованное фото')


# @router.message(F.photo)
# async def command_test_handler(message: Message, state: FSMContext) -> None:
#     await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
#     file_id = message.photo[-1].file_id
#
#     image = BytesIO()
#     await message.bot.download(file=file_id, destination=image)
#     await state.update_data(human_img=image.getvalue())
#
#     await message.reply_document(
#         document=types.BufferedInputFile(
#             file=image.getvalue(),
#             filename='Результат.jpeg'
#         )
#     )



@router.callback_query(F.data == 'send_photo')
async def send_photo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Photo.human_img)
    await callback.answer('Отправьте ваше фото')
    await callback.message.edit_text('Отправьте ваше фото:', reply_markup=await kb.exit())



@router.message(Photo.human_img, F.photo)
async def get_human_img(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    human_img = io.BytesIO()

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    await message.bot.download(file=file_id, destination=human_img)
    await state.update_data(human_img=human_img)

    await state.set_state(Photo.garm_img)
    await message.answer(text='Пришлите фото одежды:', reply_markup=await kb.exit())


@router.message(Photo.garm_img, F.photo)
async def get_garm_img(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    garm_img = io.BytesIO()

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    await message.bot.download(file=file_id, destination=garm_img)
    await state.update_data(garm_img=garm_img)
    await send_image(message, state)

    # await state.clear()


async def send_image(message, state):
    await message.answer(text=f'Подождите немного...\nБот старается вас одеть 😊')
    await message.answer_dice(emoji='🎲')
    await state.set_state(Photo.waiting)

    data_images = await state.get_data()
    data_images = {
        "human_img": data_images['human_img'],
        "garm_img": data_images['garm_img'],
        "garment_des": "cute"
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
        else:
            await message.answer(text=f'К сожалению боту не удалось распознать ваши изображения.\n'
                                      f'Загрузите изображения,  на которых четко выделяются как человек, так и вещь.')
    await state.clear()




@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(f"Бот для примерки.\nНажмите 'Отправить фото' и загрузите ваше изображения",
                                     reply_markup=await kb.start())
