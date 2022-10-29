import datetime
import os
import sqlite3

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.reply import pyaterochka_menu
from tgbot.misc.get_sales_from_5ka import get_all_sales_from_all_pages_5ka, best_sales_5ka, low_prices_5ka, generate_text
from tgbot.misc.states import Stages


async def pyaterochka(message: Message):
    await message.answer('Сделайте выбор', reply_markup=pyaterochka_menu)
    await Stages.pyaterochka.set()


def register_pyaterochka(dp: Dispatcher):
    dp.register_message_handler(pyaterochka, text='Пятёрочка')


async def show_sales_5ka(message: Message, state: FSMContext):
    data = await state.get_data()
    store = data.get('city_code')
    city_short_name = data.get('city_short_name')

    if store is None:
        store = '34ID'

    if city_short_name is None:
        city_short_name = 'RND'

    today = datetime.datetime.now().strftime("%d%m%y")
    filename = f'data/P_{city_short_name}_{store}_{today}.db'

    creating_db_message = None
    if not os.path.exists(filename):
        creating_db_message = await message.answer(text='Создаём базу данных. Обычно это занимает не более 30 секунд.')
        get_all_sales_from_all_pages_5ka(filename=filename, store=store)

    if creating_db_message:
        await creating_db_message.delete()

    result_text = ''
    if message.text == 'Лучшие скидки':
        sales = best_sales_5ka(filename=filename)
        result_text += f'Самые большие скидки (первые 10): \n\n'
        result_text += generate_text(sales)
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())
        # Добавить inline кнопки: 1. Вывести остальные 2. Показывать по одному

    elif message.text == 'Низкие цены':
        result_text += 'Самые низкие цены (первые 10): \n\n'
        sales = low_prices_5ka(filename)
        result_text += generate_text(sales)
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())

    await state.reset_state(with_data=False)


def register_show_sales(dp: Dispatcher):
    dp.register_message_handler(show_sales_5ka, text=['Лучшие скидки', 'Низкие цены'], state=Stages.pyaterochka)


def register_all_stores(dp):
    register_pyaterochka(dp)
    register_show_sales(dp)
