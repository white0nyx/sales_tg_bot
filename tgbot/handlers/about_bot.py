from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message


async def about_bot(message: Message):
    """Обработка команды about_bot"""
    await message.answer(f'Пока что вы можете узнать только о том, что бота создал '
                         f'<a href="https://t.me/dmitrykotlyar">Анатолий Кушнаренко</a>.\n\n',
                         disable_web_page_preview=True)


def register_about_bot(dp: Dispatcher):
    """Регистрация обработчика команды about_bot"""
    dp.register_message_handler(about_bot, Command('about_bot'))
