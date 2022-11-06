from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message


async def help_command(message: Message):
    await message.answer('/start - запуск/перезапуск бота\n\n'
                         '/help - помощь по командам\n\n'
                         '/set_city - изменить город поиска\n\n'
                         '/set_magnet_city - установить собственный город для магазина Магнит по его коду\n'
                         '(прилагается инструкция)\n\n'
                         '/set_5ka_store - установить собственный магазин для магазина Пятёрочка по его коду\n'
                         '(прилагается инструкция)\n\n'
                         '/about_bot - получить информацию о боте')


def register_help_command(dp: Dispatcher):
    dp.register_message_handler(help_command, Command('help'))
