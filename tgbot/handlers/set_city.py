from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_datas import city_callback
from tgbot.keyboards.inline import cities_choice


async def menu_set_city(message: Message, state: FSMContext):
    data = await state.get_data()
    city_name = data.get('city_name')
    if city_name:
        await message.answer(text=f'Выбранный город: {city_name}\n'
                                  'Для изменения выбери город: ', reply_markup=cities_choice)

    else:
        await message.answer(text='Выбери свой город:', reply_markup=cities_choice)


def register_set_city(dp: Dispatcher):
    dp.register_message_handler(menu_set_city, Command('set_city'))


async def city_button(call: CallbackQuery, callback_data: dict, state: FSMContext):
    city_name = callback_data.get('city_name')
    city_code = callback_data.get('city_code')
    await call.answer(text=f'Город {city_name} успешно сохранён')

    async with state.proxy() as data:
        data['city_name'] = city_name
        data['city_code'] = city_code

    data = await state.get_data()
    cn = data.get('city_name')
    cc = data.get('city_code')
    await call.message.answer(f'Выбранный город {cn} успешно сохранён. Код магазина: {cc}\n'
                              f'Для изменения города воспользуйтесь командой /set_city')
    await call.message.delete()


def register_city_button(dp: Dispatcher):
    dp.register_callback_query_handler(city_button, city_callback.filter())


def register_all_set_city(dp):
    register_set_city(dp)
    register_city_button(dp)
