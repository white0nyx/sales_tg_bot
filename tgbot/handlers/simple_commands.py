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
        'Чтобы я показывал самые актуальные для тебя скидки, я должен знать твой город.\n'
        'Для установки города ты можешь воспользоваться командой /set_city. Если ты этого не сделаешь, '
        'я буду показывать тебе скидки в городе Ростов-на-Дону.\n\n'
        'Удачных покупок!', reply_markup=choice_company)


def register_start(dp: Dispatcher):
    """Регистрация обработчика команды start"""
    dp.register_message_handler(start, Command('start'))


async def help_command(message: Message):
    """Обработчик команды help"""
    await message.answer('/start - запуск/перезапуск бота\n\n'
                         '/help - помощь по командам\n\n'
                         '/set_city - изменить город поиска\n\n'
                         '/set_magnet_city - установить собственный город для магазина Магнит по его коду\n'
                         '(прилагается инструкция)\n\n'
                         '/set_5ka_store - установить собственный магазин для магазина Пятёрочка по его коду\n'
                         '(прилагается инструкция)\n\n'
                         '/set_count_sales - установить количество выводимых скидок за раз\n\n'
                         '/about_bot - получить информацию о боте\n\n')


def register_help_command(dp: Dispatcher):
    """Регистрация обработчика команды help"""
    dp.register_message_handler(help_command, Command('help'))


async def about_bot(message: Message):
    """Обработка команды about_bot"""
    await message.answer(f'Пока что вы можете узнать только о том, что бота создал '
                         f'<a href="https://t.me/dmitrykotlyar">Анатолий Кушнаренко</a>.\n\n',
                         disable_web_page_preview=True)


def register_about_bot(dp: Dispatcher):
    """Регистрация обработчика команды about_bot"""
    dp.register_message_handler(about_bot, Command('about_bot'))


def register_all_simple_command(dp):
    register_start(dp)
    register_help_command(dp)
    register_about_bot(dp)
