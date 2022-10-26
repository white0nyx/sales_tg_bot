from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import cities_choice


async def menu_set_city(message: Message):
    await message.answer(text='Выбери свой город: ', reply_markup=cities_choice)


def register_set_city(dp: Dispatcher):
    dp.register_message_handler(menu_set_city, Command('set_city'))


async def city_button(call: CallbackQuery):
    city = call.data
    await call.answer(text=f'Город {city} успешно сохранён')


def register_city_button(dp: Dispatcher):
    dp.register_callback_query_handler(city_button)


def register_all_set_city(dp):
    register_set_city(dp)
    register_city_button(dp)