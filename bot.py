import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from tgbot.config import load_config
from tgbot.handlers.simple_commands import register_about_bot, register_start, register_help_command, \
    register_all_simple_command
from tgbot.handlers.cancel import register_cancel
from tgbot.handlers.page_buttons import register_all_pagination
from tgbot.handlers.set_5ka_store import register_all_set_5k_store
from tgbot.handlers.set_city import register_all_set_city
from tgbot.handlers.set_count_sales import register_all_set_count_sales
from tgbot.handlers.set_magnet_city import register_all_set_magnet_city
from tgbot.handlers.stores import register_all_store

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    """Регистрация middlewares"""
    pass


def register_all_filters(dp):
    """Регистрация кастомных фильтров"""
    pass


def register_all_handlers(dp):
    """Регистрация обработчиков"""
    register_all_simple_command(dp)
    register_cancel(dp)
    register_all_set_count_sales(dp)
    register_all_set_city(dp)
    register_all_store(dp)
    register_all_set_magnet_city(dp)
    register_all_set_5k_store(dp)
    register_all_pagination(dp)


async def main():
    """Функция, создающая и запускающая бота"""
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # Регистрация меню команд
    await dp.bot.set_my_commands([BotCommand('start', 'Запустить бота'),
                                  BotCommand('help', 'Помощь по командам'),
                                  BotCommand('set_city', 'Выбрать город'),
                                  BotCommand('set_magnet_city', 'Установить конкретный магазин Магнита'),
                                  BotCommand('set_5ka_store', 'Установить конкретный магазин Пятёрочки'),
                                  BotCommand('set_count_sales', 'Установить количество выводимых скидок за раз'),
                                  BotCommand('about_bot', 'Информация о боте')])

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
