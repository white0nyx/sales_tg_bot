# Выбор магазина и его скидок

import datetime
import os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.inline import get_page_keyboard
from tgbot.keyboards.reply import choice_company, sales_keyboard
from tgbot.misc.get_sales_from_5ka import get_all_sales_from_all_pages_5ka
from tgbot.misc.get_sales_from_magnet import get_sales_from_one_page_magnet
from tgbot.misc.pages import get_page
from tgbot.misc.sql_requests import best_sales, search_by_text, low_prices
from tgbot.misc.states import Stages
from tgbot.misc.work_with_text import split_into_pages


async def store(message: Message):
    """Обработка кнопок магазинов"""
    await message.answer('🔍 Сделайте выбор или введите текст для поиска по названию товара.', reply_markup=sales_keyboard)
    if message.text == '🧲 Магнит':
        await Stages.magnet.set()

    elif message.text == '5️⃣ Пятёрочка':
        await Stages.pyaterochka.set()


def register_stores(dp: Dispatcher):
    """Регистрация обработчика кнопок магазинов"""
    dp.register_message_handler(store, text=['🧲 Магнит', '5️⃣ Пятёрочка'])


async def show_sales(message: Message, state: FSMContext):
    """Обработчик нажатия на кнопки скидок или поиска по названию
    Вывод скидок по указанному запросу"""
    data = await state.get_data()

    store_code = None
    store_letter = None
    get_sales_func = None
    pages = None
    if await state.get_state() == Stages.magnet.state:
        store_code = data.get('magnet_code')
        if store_code is None:
            store_code = '1452'
        store_letter = 'M'
        get_sales_func = get_sales_from_one_page_magnet

    elif await state.get_state() == Stages.pyaterochka.state:
        store_code = data.get('pyaterochka_code')
        if store_code is None:
            store_code = '34ID'
        store_letter = 'P'
        get_sales_func = get_all_sales_from_all_pages_5ka

    city_short_name = data.get('city_short_name')
    if city_short_name is None:
        city_short_name = 'RND'

    today = datetime.datetime.now().strftime("%d%m%y")
    filename = f'data/{store_letter}_{city_short_name}_{store_code}_{today}.db'

    count_sales = data.get('count_sales')

    if count_sales is None:
        count_sales = 10

    creating_db_message = None
    if not os.path.exists(filename):
        creating_db_message = await message.answer(
            text=f'⚒ Создаём базу данных. Это может занять несколько минут.',
            reply_markup=ReplyKeyboardRemove())
        get_sales_func(filename=filename, store=store_code)

    if creating_db_message:
        await creating_db_message.delete()

    if message.text == '💯 Лучшие скидки':
        result_text = f'🔥 <b>Топ самых больших скидок</b>\n\n'
        sales = best_sales(filename=filename)
        pages = split_into_pages(sales, count_sales)
        result_text += get_page(pages)

    elif message.text == '📉 Низкие цены':
        result_text = f'🔥 <b>Топ самых дешёвых товаров</b>\n\n'
        sales = low_prices(filename)
        pages = split_into_pages(sales, count_sales)
        result_text += get_page(pages)

    else:
        sales = search_by_text(filename=filename, request=message.text)
        if len(sales) == 0:
            result_text = 'По вашему запросу скидок не обнаружено'
        else:
            result_text = f'🔥 <b>Скидки по вашему запросу</b>\n\n'
            pages = split_into_pages(sales, count_sales)
            result_text += get_page(pages)

            await message.answer(result_text, reply_markup=choice_company)
            return

    if len(sales) <= count_sales:
        await message.answer(text=result_text, reply_markup=sales_keyboard)

    else:
        await message.answer(text=result_text, reply_markup=get_page_keyboard(max_pages=len(sales), key='sales'))
        await message.answer(f'✅ Мы нашли {len(sales)} скидок для вас!\n'
                             f'Количество страниц: {len(pages)}', reply_markup=choice_company)

        async with state.proxy() as data:
            data['pages'] = pages

        await state.reset_state(with_data=False)


def register_show_sales(dp: Dispatcher):
    """Регистрация обработчика нажатия на кнопки скидок или поиска по названию"""
    dp.register_message_handler(callback=show_sales,
                                state=[Stages.magnet, Stages.pyaterochka])


def register_all_store(dp):
    """Регистрация всех обработчиков связанных с выбором магазина и выводом скидок"""
    register_stores(dp)
    register_show_sales(dp)
