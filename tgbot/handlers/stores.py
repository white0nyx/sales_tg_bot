import datetime
import os
import sqlite3

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import pyaterochka_menu
from tgbot.misc.get_sales import get_all_sales_from_all_pages, best_sales, low_prices
from tgbot.misc.states import Stages


async def pyaterochka(message: Message, state: FSMContext):
    await message.answer('Сделайте выбор', reply_markup=pyaterochka_menu)
    await Stages.pyaterochka.set()


def register_pyaterochka(dp: Dispatcher):
    dp.register_message_handler(pyaterochka, text='Пятёрочка')


async def show_sales(message: Message, state: FSMContext):
    data = await state.get_data()
    store = data.get('city_code')
    if store is None:
        store = '34ID'

    today = datetime.datetime.now().strftime("%d%m%y")
    filename = f'data/{store}_{today}.db'

    if not os.path.exists(filename):
        get_all_sales_from_all_pages(filename=filename, store=store)

    if message.text == 'Лучшие скидки':
        pass

    elif message.text == 'Низкие цены':
        pass

    await state.finish()


def register_show_sales(dp: Dispatcher):
    dp.register_message_handler(show_sales, text='Лучшие скидки', state=Stages.pyaterochka)


def register_all_stores(dp):
    register_pyaterochka(dp)
    register_show_sales(dp)
