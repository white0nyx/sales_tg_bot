# Обработка кнопки Отмена

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import choice_company
from tgbot.misc.states import Stages


async def cancel(message: Message, state: FSMContext):
    """Обработка кнопки Отмена"""
    await state.reset_state(with_data=False)
    await message.answer('Вы вернулись в главное меню', reply_markup=choice_company)


def register_cancel(dp: Dispatcher):
    """Регистрация обработчика кнопки Отмена"""
    dp.register_message_handler(callback=cancel,
                                text='↩ Отмена',
                                state=[Stages.set_magnet_city,
                                       Stages.set_5k_store,
                                       Stages.set_count_sales,
                                       Stages.magnet,
                                       Stages.pyaterochka,
                                       Stages.feedback])
