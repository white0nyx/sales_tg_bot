import datetime
import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.get_sales import get_all_sales_from_all_pages


async def pyaterochka(message: Message, state: FSMContext):
    data = await state.get_data()
    store = data.get('city_code')
    today = datetime.datetime.now().strftime("%d%m%y")
    filename = f'data/{store}_{today}.db'

    if os.path.exists(filename):
        await message.answer('Файл существует')

    else:
        await message.answer('Файл не найден')
        get_all_sales_from_all_pages(filename=filename, store=store)


def register_pyaterochka(dp: Dispatcher):
    dp.register_message_handler(pyaterochka, text='Пятёрочка')


def register_all_stores(dp):
    register_pyaterochka(dp)