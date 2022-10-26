from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice_company = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Пятёрочка'),
        KeyboardButton(text='Магнит')
    ]
], resize_keyboard=True)