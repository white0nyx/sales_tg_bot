import datetime
import os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.reply import magnet_menu
from tgbot.misc.get_sales_from_5ka import best_sales_5ka, generate_text, low_prices_5ka
from tgbot.misc.get_sales_from_magnet import get_sales_from_one_page_magnet
from tgbot.misc.states import Stages


async def magnet(message: Message):
    await message.answer('Сделайте выбор', reply_markup=magnet_menu)
    await Stages.magnet.set()


def register_magnet(dp: Dispatcher):
    dp.register_message_handler(magnet, text='Магнит')


async def show_sales_magnet(message: Message, state: FSMContext):
    data = await state.get_data()
    store = data.get('magnet_code')

    city_short_name = data.get('city_short_name')

    if store is None:
        store = '1452'

    if city_short_name is None:
        city_short_name = 'RND'

    today = datetime.datetime.now().strftime("%d%m%y")
    filename = f'data/M_{city_short_name}_{store}_{today}.db'

    creating_db_message = None
    if not os.path.exists(filename):
        creating_db_message = await message.answer(text='Создаём базу данных. Обычно это занимает не более 2 минут.')
        get_sales_from_one_page_magnet(filename=filename, store=store)

    if creating_db_message:
        await creating_db_message.delete()

    result_text = ''
    if message.text == 'Лучшие скидки':
        sales = best_sales_5ka(filename=filename)
        result_text += f'Самые большие скидки (первые 10): \n\n'
        result_text += generate_text(sales)
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Низкие цены':
        result_text += 'Самые низкие цены (первые 10): \n\n'
        sales = low_prices_5ka(filename)
        result_text += generate_text(sales)
        await message.answer(text=result_text, reply_markup=ReplyKeyboardRemove())

    await state.reset_state(with_data=False)


def register_show_sales_magnet(dp: Dispatcher):
    dp.register_message_handler(show_sales_magnet, text=['Лучшие скидки', 'Низкие цены'], state=Stages.magnet)


def register_all_magnet(dp):
    register_magnet(dp)
    register_show_sales_magnet(dp)
