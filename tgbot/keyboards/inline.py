# Inline клавиатуры

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import city_callback, pagination_call

# Клавиатура с выбором города
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

# Кнопки - "Да", "Нет"
yes_no_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='yes'),
        InlineKeyboardButton(text='Нет', callback_data='no')
    ]
])


def get_page_keyboard(max_pages: int, key: str, page: int = 1):
    """Формирование клавиатуры с пагинацией"""
    previous_page = page - 1
    previous_page_text = '<< '

    current_page_text = f'<{page}>'

    next_page = page + 1
    next_page_text = ' >>'

    markup = InlineKeyboardMarkup()

    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_call.new(key=key, page='current_page')
        )
    )

    if next_page < max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page)
            )
        )

    return markup


# Кнопка с инструкцией для установки магазина Магнита
instruction_magnet = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📜 Инструкция', url='https://www.notion.so/ab6bca8ca72e44c0969c0e61166d8e72')
    ]
])

# Кнопка с инструкцией для установки магазина Пятёрочки
instruction_5ka = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📜 Инструкция',
                             url='https://curly-surfboard-74f.notion.site/44c0bb27e15c441da8e889f7bd28f6e4')
    ]
])
