import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from tgbot.config import load_config
from tgbot.handlers.about_bot import register_about_bot
from tgbot.handlers.set_city import register_all_set_city
from tgbot.handlers.set_magnet_city import register_all_set_magnet_store, register_cancel
from tgbot.handlers.start import register_start
from tgbot.handlers.stores import register_all_store

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    pass


def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_start(dp)
    register_all_set_city(dp)
    register_about_bot(dp)
    register_all_store(dp)
    register_all_set_magnet_store(dp)


async def main():
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

    await dp.bot.set_my_commands([BotCommand('start', 'Запустить бота'),
                                  BotCommand('set_city', 'Выбрать город'),
                                  BotCommand('set_magnet_city', 'Установить конкретный магазин Магнита'),
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
