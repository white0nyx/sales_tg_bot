from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import city_callback

cities_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Москва', callback_data=city_callback.new(city_name='Москва')),
        InlineKeyboardButton(text='Санкт-Петербург', callback_data=city_callback.new(city_name='Санкт-Петербург'))
    ],
    [
        InlineKeyboardButton(text='Краснодар', callback_data=city_callback.new(city_name='Краснодар')),
        InlineKeyboardButton(text='Ростов-на-Дону', callback_data=city_callback.new(city_name='Ростов-на-Дону'))
    ]
])
