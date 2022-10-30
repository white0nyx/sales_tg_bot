import datetime
import os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.reply import magnet_menu
from tgbot.misc.get_sales_from_5ka import best_sales, generate_text, low_prices, \
    get_all_sales_from_all_pages_5ka
from tgbot.misc.get_sales_from_magnet import get_sales_from_one_page_magnet
from tgbot.misc.states import Stages


async def store(message: Message):
    await message.answer('Сделайте выбор', reply_markup=magnet_menu)
    if message.text == 'Магнит':
        await Stages.magnet.set()

    elif message.text == 'Пятёрочка':
        await Stages.pyaterochka.set()


def register_stores(dp: Dispatcher):
    dp.register_message_handler(store, text=['Магнит', 'Пятёрочка'])


async def show_sales(message: Message, state: FSMContext):
    data = await state.get_data()

    store_code = None
    store_letter = None
    waiting_time = None
    get_sales_func = None
    if await state.get_state() == Stages.magnet.state:
        store_code = data.get('magnet_code')
        if store_code is None:
            store_code = '1452'
        store_letter = 'M'
        waiting_time = '2 минут'
        get_sales_func = get_sales_from_one_page_magnet

    elif await state.get_state() == Stages.pyaterochka.state:
        store_code = data.get('pyaterochka_code')
        if store_code is None:
            store_code = '34ID'
        store_letter = 'P'
        waiting_time = '30 секунд'
        get_sales_func = get_all_sales_from_all_pages_5ka

    city_short_name = data.get('city_short_name')

    if city_short_name is None:
        city_short_name = 'RND'

    today = datetime.datetime.now().strftime("%d%m%y")
    filename = f'data/{store_letter}_{city_short_name}_{store_code}_{today}.db'

    creating_db_message = None
    if not os.path.exists(filename):
        creating_db_message = await message.answer(
            text=f'Создаём базу данных. Обычно это занимает не более {waiting_time}.')
        get_sales_func(filename=filename, store=store_code)

    if creating_db_message:
        await creating_db_message.delete()

    result_text = ''
    if message.text == 'Лучшие скидки':
        sales = best_sales(filename=filename)
        result_text += f'Самые большие скидки (первые 10): \n\n'
        result_text += generate_text(sales)
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Низкие цены':
        result_text += 'Самые низкие цены (первые 10): \n\n'
        sales = low_prices(filename)
        result_text += generate_text(sales)
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())

    await state.reset_state(with_data=False)


def register_show_sales(dp: Dispatcher):
    dp.register_message_handler(callback=show_sales,
                                text=['Лучшие скидки', 'Низкие цены'],
                                state=[Stages.magnet, Stages.pyaterochka])


def register_all_store(dp):
    register_stores(dp)
    register_show_sales(dp)
