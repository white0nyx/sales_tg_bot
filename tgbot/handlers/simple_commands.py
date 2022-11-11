# Простые команды

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot.keyboards.reply import choice_company


async def start(message: Message):
    """Обработка команды start"""
    await message.answer('👋')
    await message.answer(
        'Привет! Я бот, который расскажет тебе о самых крупных скидках магазинов Пятёрочка и Магнит.\n\n'
        'Чтобы я показывал самые актуальные для тебя скидки, я должен знать твой город.\n\n'
        'Для установки города ты можешь воспользоваться командой <b><i>/set_city</i></b>.\n'
        'По умолчанию я показываю скидки в городе Ростов-на-Дону.\n\n'
        'Удачных покупок! 🛍', reply_markup=choice_company)


def register_start(dp: Dispatcher):
    """Регистрация обработчика команды start"""
    dp.register_message_handler(start, Command('start'))


async def help_command(message: Message):
    """Обработчик команды help"""
    await message.answer('<b>💡 /Имеющиеся команды и их функции:</b>\n\n'
                         '<b><i>/start</i></b> - запуск/перезапуск бота\n\n'
                         '<b><i>/help</i></b> - помощь по командам\n\n'
                         '<b><i>/set_city</i></b> - изменить город поиска\n\n'
                         '<b><i>/set_magnet_city</i></b> - установить собственный город для магазина Магнит по его коду\n'
                         '(прилагается инструкция)\n\n'
                         '<b><i>/set_5ka_store</i></b> - установить собственный магазин для магазина Пятёрочка по его коду\n'
                         '(прилагается инструкция)\n\n'
                         '<b><i>/set_count_sales</i></b> - установить количество выводимых скидок за раз\n\n'
                         '<b><i>/about_bot</i></b> - получить информацию о боте\n\n'
                         '❕<i>(Все команды необходимо использовать в начальном меню)</i>')


def register_help_command(dp: Dispatcher):
    """Регистрация обработчика команды help"""
    dp.register_message_handler(help_command, Command('help'))


async def about_bot(message: Message):
    """Обработка команды about_bot"""
    await message.answer(f'💎 Пока что вы можете узнать только о том, что бота создал '
                         f'<a href="https://t.me/dmitrykotlyar">Анатолий Кушнаренко</a>.\n\n',
                         disable_web_page_preview=True)


def register_about_bot(dp: Dispatcher):
    """Регистрация обработчика команды about_bot"""
    dp.register_message_handler(about_bot, Command('about_bot'))


def register_all_simple_command(dp):
    register_start(dp)
    register_help_command(dp)
    register_about_bot(dp)
