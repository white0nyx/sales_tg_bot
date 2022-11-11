# Установка своего магазина Пятёрочки

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import yes_no_buttons, instruction_5ka
from tgbot.keyboards.reply import cancel_button, choice_company
from tgbot.misc.get_sales_from_5ka import check_5ka_store_code
from tgbot.misc.states import Stages


async def set_5ka_store_command(message: Message):
    """Обработка команды set_5ka_store"""
    await message.answer('❓ Укажите код конкретного магазина Пятёрочка', reply_markup=instruction_5ka)
    await message.answer('⚠ Вы можете воспользоваться инструкцией по кнопке выше', reply_markup=cancel_button)
    await Stages.set_5k_store.set()


def register_set_5ka_store_command(dp: Dispatcher):
    """Регистрация обработчика команды set_5ka_store"""
    dp.register_message_handler(set_5ka_store_command, Command('set_5ka_store'))


async def check_5ka_store(message: Message, state: FSMContext):
    """Обработка указанного кода магазина"""
    store_code = message.text
    store = check_5ka_store_code(store_code)

    if store is None:
        await message.answer(f'❌ Магазин с кодом {store_code} не обнаружен, проверьте правильность введённых данных.',
                             reply_markup=cancel_button)

    else:
        async with state.proxy() as data:
            data['suspect_city'] = store
            data['suspect_city_code'] = store_code

        await message.answer(text=f'{store}\n\n'
                                  f'Адрес найден верно?',
                             reply_markup=yes_no_buttons)


def register_check_5ka_store(dp: Dispatcher):
    """Регистрация обработчика указанного кода магазина"""
    dp.register_message_handler(check_5ka_store, state=Stages.set_5k_store)


async def set_store_5ka(call: CallbackQuery, state: FSMContext):
    """Обработка нажатия на кнопки подтверждения подозреваемого магазина"""
    await call.answer(cache_time=30)
    store = call.message.text.split('\n\n')[0]

    if call.data == 'no':
        await set_5ka_store_command(call.message)
        await call.message.delete()

    else:
        async with state.proxy() as data:
            data['pyaterochka_code'] = data['suspect_city_code']
            del data['suspect_city_code']
            del data['suspect_city']
            await state.reset_state(with_data=False)
            await call.message.answer(f'✅ Адрес {store} для магазина Пятёрочка установлен',
                                      reply_markup=choice_company)


def register_set_store_5ka(dp: Dispatcher):
    """Регистрация обработчика кнопок подтверждения"""
    dp.register_callback_query_handler(set_store_5ka, state=Stages.set_5k_store)


def register_all_set_5k_store(dp):
    """Регистрация всех обработчиков связанных с установкой магазина Пятёрочки"""
    register_set_5ka_store_command(dp)
    register_check_5ka_store(dp)
    register_set_store_5ka(dp)
