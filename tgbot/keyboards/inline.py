from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import city_callback

cities_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Москва', callback_data=city_callback.new(city_name='Москва',
                                                                            pyaterochka_code='S801',
                                                                            magnet_code='2398',
                                                                            city_short_name='MSC')),

        InlineKeyboardButton(text='Санкт-Петербург', callback_data=city_callback.new(city_name='Санкт-Петербург',
                                                                                     pyaterochka_code='5599',
                                                                                     magnet_code='1645',
                                                                                     city_short_name='SBP'))
    ],
    [
        InlineKeyboardButton(text='Краснодар', callback_data=city_callback.new(city_name='Краснодар',
                                                                               pyaterochka_code='308R',
                                                                               magnet_code='1761',
                                                                               city_short_name='KRD')),

        InlineKeyboardButton(text='Ростов-на-Дону', callback_data=city_callback.new(city_name='Ростов-на-Дону',
                                                                                    pyaterochka_code='34ID',
                                                                                    magnet_code='1452',
                                                                                    city_short_name='RND'))
    ]
])
