from aiogram.dispatcher.filters.state import StatesGroup, State


class Stages(StatesGroup):
    pyaterochka = State()
    magnet = State()
    set_magnet_city = State()
    set_5k_store = State()
