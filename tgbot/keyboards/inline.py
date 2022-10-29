from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import city_callback

cities_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Москва', callback_data=city_callback.new(city_name='Москва',
                                                                            city_code='S801',
                                                                            city_short_name='MSC')),

        InlineKeyboardButton(text='Санкт-Петербург', callback_data=city_callback.new(city_name='Санкт-Петербург',
                                                                                     city_code='5599',
                                                                                     city_short_name='SBP'))
    ],
    [
        InlineKeyboardButton(text='Краснодар', callback_data=city_callback.new(city_name='Краснодар',
                                                                               city_code='308R',
                                                                               city_short_name='KRD')),

        InlineKeyboardButton(text='Ростов-на-Дону', callback_data=city_callback.new(city_name='Ростов-на-Дону',
                                                                                    city_code='34ID',
                                                                                    city_short_name='RND'))
    ]
])
