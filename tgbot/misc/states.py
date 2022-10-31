from aiogram.dispatcher.filters.state import StatesGroup, State


class Stages(StatesGroup):
    pyaterochka = State()
    magnet = State()
    set_magnet_store = State()