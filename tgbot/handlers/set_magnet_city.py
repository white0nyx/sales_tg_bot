from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import yes_no_buttons
from tgbot.keyboards.reply import cancel_button, choice_company
from tgbot.misc.get_sales_from_magnet import check_magnet_city_code
from tgbot.misc.states import Stages


async def set_magnet_store_command(message: Message):
    await message.answer('Укажите код конкретного магазина Магнит', reply_markup=cancel_button)
    await Stages.set_magnet_store.set()


def register_set_magnet_store_command(dp: Dispatcher):
    dp.register_message_handler(set_magnet_store_command, Command('set_magnet_city'))


async def cancel(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await message.answer('Вы вернулись в главное меню', reply_markup=choice_company)


def register_cancel(dp: Dispatcher):
    dp.register_message_handler(cancel, text='Отмена', state=Stages.set_magnet_store)


async def check_magnet_store(message: Message, state: FSMContext):
    city_code = message.text
    city = check_magnet_city_code(city_code)

    if city is None:
        await message.answer(f'Город с кодом {city_code} не обнаружен, проверьте правильность введённых данных.',
                             reply_markup=cancel_button)

    else:
        async with state.proxy() as data:
            data['suspect_city'] = city
            data['suspect_city_code'] = city_code

        await message.answer(f'Ваш населённый пункт - {city}?',
                             reply_markup=yes_no_buttons)


def register_check_magnet_store(dp: Dispatcher):
    dp.register_message_handler(check_magnet_store, state=Stages.set_magnet_store)


async def set_city_magnet(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=30)
    city = call.message.text.split()[-1][:-1]
    if call.data == 'no':
        await set_magnet_store_command(call.message)
        await call.message.delete()

    else:
        async with state.proxy() as data:
            data['magnet_code'] = data['suspect_city_code']
            del data['suspect_city_code']
            del data['suspect_city']
            await state.reset_state(with_data=False)
            await call.message.answer(f'Населённый пункт {city} для магазина Магнит установлен',
                                      reply_markup=choice_company)


def register_set_city_magnet(dp: Dispatcher):
    dp.register_callback_query_handler(set_city_magnet, state=Stages.set_magnet_store)


def register_all_set_magnet_store(dp):
    register_set_magnet_store_command(dp)
    register_cancel(dp)
    register_check_magnet_store(dp)
    register_set_city_magnet(dp)
