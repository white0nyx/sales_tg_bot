# Создание стейтов

from aiogram.dispatcher.filters.state import StatesGroup, State


class Stages(StatesGroup):
    """Класс стейтов"""
    pyaterochka = State()
    magnet = State()
    set_magnet_city = State()
    set_5k_store = State()
    set_count_sales = State()
    feedback = State()
