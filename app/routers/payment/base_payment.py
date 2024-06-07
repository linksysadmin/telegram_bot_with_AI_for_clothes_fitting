from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import LabeledPrice

from config import PAYMENT_TOKEN
import logging

from aiogram import Bot, Dispatcher, types, Router, F

router = Router()


# покупка / buy command
@router.message(Command('buy'))
async def buy(message: types.Message, bot: Bot):

    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка генераций',
        description='Активация  генераций',
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        # is_flexible=False,
        prices=[
            LabeledPrice(label=f'Генерации', amount=100*100),
        ],
        # start_parameter='Канал',
        payload='test-invoice-payload',
        # request_timeout=15,

    )


# пре-чекаут (ответ серверу должен быть отправлен в течение 10 секунд, иначе платеж не пройдет) / pre-checkout
@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# успешная оплата / successful payment
@router.message(F.successful_payment)
async def successful_payment(message: types.Message, bot: Bot):
    await bot.send_message(message.chat.id,
                           f"Оплата на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошла успешно!")


@router.message(F.successful_payment)
async def successful_payment(message: types.Message, bot: Bot):
    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")




