from aiogram import html, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards as kb
from states import Photo

router = Router(name=__name__)


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


