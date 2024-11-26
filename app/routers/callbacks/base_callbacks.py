from aiogram import html, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app import keyboards as kb
from app.filters.user_filters import AvailableGeneration
from app.keyboards import ClothType
from app.routers.payment.base_payment import invoice
from app.templates.messages_templates import MESSAGE_HELP
from app.states import Photo


router = Router(name=__name__)


@router.callback_query(kb.ClothTypeCallbackData.filter(), AvailableGeneration())
async def handler_type_cloth_callback(callback: CallbackQuery,
                                      callback_data: kb.ClothTypeCallbackData,
                                      state: FSMContext) -> None:
    """
    Отрабатывает на нажатие кнопки одной из категорий примерки, при достаточном кол-ве генераций
    :param callback: Callback запрос
    :param callback_data: Строка-запроса сформированная для кнопки на клавиатуре
    :param state: Состояние
    """
    await state.update_data(cloth=callback_data.cloth)
    await state.set_state(Photo.human_img)

    for type in ClothType:
        if type.name == callback_data.cloth:
            await callback.message.edit_text(f'Категория:\n{html.bold(type.value)}\n\n'
                                             f'1️⃣ Загрузите изображение человека', reply_markup=await kb.cancel())


@router.callback_query(kb.ClothTypeCallbackData.filter(), ~AvailableGeneration())
async def handler_type_cloth_callback(callback: CallbackQuery) -> None:
    """
    Отрабатывает на нажатие кнопки одной из категорий примерки, при недостаточном кол-ве генераций
    :param callback: Callback запрос
    """
    await callback.message.edit_text(f'У вас нет доступных генераций\n'
                                     f'Выберите:', reply_markup=await kb.generations())


@router.callback_query(kb.GenerationAmountCallbackData.filter())
async def buy(callback: CallbackQuery,
              callback_data: kb.GenerationAmountCallbackData,
              state: FSMContext) -> None:
    """
    Отрабатывает на выбор определенного кол-ва генераций при покупке, а также добавляет это количество в кэш
    :param callback: Callback запрос
    :param callback_data: Строка-запроса сформированная для кнопки на клавиатуре
    """
    await callback.message.delete()
    gen_amount = callback_data.gen_amount
    price = callback_data.price
    await state.update_data(gen_amount=gen_amount)
    await invoice(callback, price=price)


@router.callback_query(F.data == 'cancel')
async def handler_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Отрабатывает на нажатие кнопки 'Отмена'
    :param callback: Callback запрос
    :param state: Состояние
    """
    await state.clear()
    await callback.message.edit_text(MESSAGE_HELP, reply_markup=await kb.clothing_types())
