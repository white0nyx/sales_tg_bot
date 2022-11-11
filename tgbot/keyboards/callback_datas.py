from aiogram.utils.callback_data import CallbackData

# CallbackData для кнопок города
city_callback = CallbackData('city', 'city_name', 'pyaterochka_code', 'magnet_code', 'city_short_name')

# CallbackData для кнопок пагинации
pagination_call = CallbackData('paginator', 'key', 'page')