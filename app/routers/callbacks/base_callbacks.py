from aiogram import html, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app import keyboards as kb
from app.filters.group_chat import IsSubscriber
from app.keyboards import ClothType
from app.templates.messages_templates import MESSAGE_HELP, NOT_SUB_MESSAGE
from app.states import Photo

router = Router(name=__name__)


@router.callback_query(kb.ClothTypeCallbackData.filter(), IsSubscriber())
async def handler_type_cloth_callback(callback: CallbackQuery, callback_data: kb.ClothTypeCallbackData,
                                      state: FSMContext):
    await state.update_data(cloth=callback_data.cloth)
    await state.set_state(Photo.human_img)
    await callback.answer('1️⃣ Загрузите изображение человека')
    for type in ClothType:
        if type.name == callback_data.cloth:
            await callback.message.edit_text(f'Категория:\n{html.bold(type.value)}\n\n'
                                             f'1️⃣ Загрузите изображение человека', reply_markup=await kb.cancel())


@router.callback_query(kb.ClothTypeCallbackData.filter())
async def handler_type_cloth_callback(callback: CallbackQuery):
    await callback.message.edit_text(NOT_SUB_MESSAGE, reply_markup=await kb.cancel())


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(MESSAGE_HELP, reply_markup=await kb.clothing_types())
