from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки выбора магазина
choice_company = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Пятёрочка'),
        KeyboardButton(text='Магнит')
    ]
], resize_keyboard=True)

# Кнопки выбора скидок для Пятёрочки
pyaterochka_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Лучшие скидки')
    ],
    [
        KeyboardButton('Низкие цены')
    ]
], resize_keyboard=True)

# Кнопки выбора скидок для Магнита
magnet_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Лучшие скидки')
    ],
    [
        KeyboardButton('Низкие цены')
    ]
], resize_keyboard=True)

# Кнопка Отмена
cancel_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Отмена')
    ]
], resize_keyboard=True)