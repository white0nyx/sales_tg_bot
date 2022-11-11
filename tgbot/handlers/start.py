from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot.keyboards.reply import choice_company


async def start(message: Message):
    """Обработка команды start"""
    await message.answer('👋')
    await message.answer('Привет! Я бот, который расскажет тебе о самых крупных скидках магазинов Пятёрочка и Магнит.\n\n'
                         'Чтобы я показывал самые актуальные для тебя скидки, я должен знать твой город.\n'
                         'Для установки города ты можешь воспользоваться командой /set_city. Если ты этого не сделаешь, '
                         'я буду показывать тебе скидки в городе Ростов-на-Дону.\n\n'
                         'Удачных покупок!', reply_markup=choice_company)


def register_start(dp: Dispatcher):
    """Регистрация обработчика команды start"""
    dp.register_message_handler(start, Command('start'))
