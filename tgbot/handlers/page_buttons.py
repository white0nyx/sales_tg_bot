from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.callback_datas import pagination_call
from tgbot.keyboards.inline import get_page_keyboard
from tgbot.misc.pages import get_page


async def current_page_button(call: CallbackQuery):
    """Обработка нажатия на кнопку текущей страницы"""
    await call.answer(cache_time=120)


def register_current_page_button(dp: Dispatcher):
    """Регистрация обработчика нажатия на кнопку текущей страницы"""
    dp.register_callback_query_handler(current_page_button, pagination_call.filter(page='current_page'))


async def show_chosen_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Обработка нажатия на кнопки переключения страниц"""
    data = await state.get_data()
    pages = data.get('pages')
    current_page = int(callback_data.get('page'))
    text = get_page(pages, page=current_page)

    markup = get_page_keyboard(max_pages=len(pages), key='sales', page=current_page)

    await call.message.edit_text(text=text, reply_markup=markup)


def register_show_chosen_page(dp: Dispatcher):
    """Регистрация обработчика нажатия на кнопки переключения страниц"""
    dp.register_callback_query_handler(show_chosen_page, pagination_call.filter(key='sales'))


def register_all_pagination(dp):
    """Регистрация всех обработчиков связанных с пагинацией"""
    register_current_page_button(dp)
    register_show_chosen_page(dp)
