from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message


async def start(message: Message):
    await message.answer('👋')
    await message.answer('Привет! Я бот, который расскажет тебе о самых крупных скидках магазинов Пятёрочка и Магнит.\n\n'
                         'Чтобы я показывал самые актуальные для тебя скидки, я должен знать твой город.\n'
                         'Для установки города ты можешь воспользоваться командой /set_city. Если ты этого не сделаешь, '
                         'я буду показывать тебе скидки в городе Ростов-на-Дону.\n\n'
                         'Удачных покупок!')


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, Command('start'))
