import datetime
import os
import sqlite3

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

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

    creating_db_message = None
    if not os.path.exists(filename):
        creating_db_message = await message.answer(text='Создаём базу данных. Обычно это занимает не более 30 секунд.')
        get_all_sales_from_all_pages(filename=filename, store=store)

    if creating_db_message:
        await creating_db_message.delete()

    result_text = ''
    if message.text == 'Лучшие скидки':
        result_text += 'Самые большие скидки (первые 10): \n\n'
        sales = best_sales(filename=filename)
        for sale in sales[:10]:
            result_text += f'🔸 {sale[1]} |\n {sale[8]}% | <s>{sale[6]}</s> ➡ <b>{sale[7]} руб.</b>\n\n'
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())
        # Добавить inline кнопки: 1. Вывести остальные 2. Показывать по одному

    elif message.text == 'Низкие цены':
        result_text += 'Самые низкие цены (первые 10): \n\n'
        sales = low_prices(filename)
        for sale in sales[:10]:
            result_text += f'🔸 {sale[1]} |\n {sale[8]}% | <s>{sale[6]}</s> ➡ <b>{sale[7]} руб.</b>\n\n'
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())

    await state.reset_state(with_data=False)


def register_show_sales(dp: Dispatcher):
    dp.register_message_handler(show_sales, text=['Лучшие скидки', 'Низкие цены'], state=Stages.pyaterochka)


def register_all_stores(dp):
    register_pyaterochka(dp)
    register_show_sales(dp)
