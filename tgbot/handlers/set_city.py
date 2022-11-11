# Установка города из предложенных

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_datas import city_callback
from tgbot.keyboards.inline import cities_choice
from tgbot.keyboards.reply import choice_company


async def menu_set_city(message: Message, state: FSMContext):
    """Обработка команды set_city"""
    data = await state.get_data()
    city_name = data.get('city_name')
    if city_name:
        await message.answer(text=f'Выбранный город: {city_name}\n'
                                  'Для изменения выбери город: ', reply_markup=cities_choice)

    else:
        await message.answer(text='Выбери свой город:', reply_markup=cities_choice)


def register_set_city(dp: Dispatcher):
    """Регистрация обработчика команды set_city"""
    dp.register_message_handler(menu_set_city, Command('set_city'))


async def city_button(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Обработка нажатия на кнопку города"""
    city_name = callback_data.get('city_name')
    pyaterochka_code = callback_data.get('pyaterochka_code')
    magnet_code = callback_data.get('magnet_code')
    city_short_name = callback_data.get('city_short_name')

    await call.answer(text=f'Город {city_name} успешно сохранён')

    async with state.proxy() as data:
        data['pyaterochka_code'] = pyaterochka_code
        data['magnet_code'] = magnet_code
        data['city_short_name'] = city_short_name

    await call.message.answer(f'Выбранный город {city_name} успешно сохранён.\n\n'
                              f'Для изменения города воспользуйтесь командой /set_city',
                              reply_markup=choice_company)
    await call.message.delete()


def register_city_button(dp: Dispatcher):
    """Регистрация обработчика кнопки города"""
    dp.register_callback_query_handler(city_button, city_callback.filter())


def register_all_set_city(dp):
    """Регистрация всех обработчиков, связанных с установкой города"""
    register_set_city(dp)
    register_city_button(dp)
