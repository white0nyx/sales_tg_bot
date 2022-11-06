from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot.keyboards.reply import cancel_button, choice_company
from tgbot.misc.states import Stages


async def set_count_sales_command(message: Message):
    await message.answer(text='Здесь вы можете указать, сколько товаров хотите видеть при выводе скидок.\n'
                              'Возможные значения находятся в промежутке от 1 до 30 включительно',
                         reply_markup=cancel_button)

    await Stages.set_count_sales.set()


def register_set_count_sales_command(dp: Dispatcher):
    dp.register_message_handler(set_count_sales_command, Command('set_count_sales'))


async def set_count_sales(message: Message, state: FSMContext):
    text = message.text

    try:
        count_sales = int(text)
        if not (1 <= count_sales <= 30):
            await message.answer('🛑 Неверно указано значение',
                                 reply_markup=cancel_button)

        else:

            async with state.proxy() as data:
                data['count_sales'] = int(text)

            await message.answer('✅ Значение сохранено', reply_markup=choice_company)
            await state.reset_state(with_data=False)

    except ValueError:
        await message.answer('🛑 Неверно указано значение',
                             reply_markup=cancel_button)


def register_set_count_sales(dp: Dispatcher):
    dp.register_message_handler(set_count_sales, state=Stages.set_count_sales)


def register_all_set_count_sales(dp):
    register_set_count_sales_command(dp)
    register_set_count_sales(dp)
