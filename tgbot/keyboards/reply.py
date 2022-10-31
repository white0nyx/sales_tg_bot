from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice_company = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Пятёрочка'),
        KeyboardButton(text='Магнит')
    ]
], resize_keyboard=True)


pyaterochka_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Лучшие скидки')
    ],
    [
        KeyboardButton('Низкие цены')
    ]
], resize_keyboard=True)


magnet_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Лучшие скидки')
    ],
    [
        KeyboardButton('Низкие цены')
    ]
], resize_keyboard=True)


cancel_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Отмена')
    ]
], resize_keyboard=True)