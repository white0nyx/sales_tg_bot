# Вся работа с текстом

import sqlite3


def best_sales(filename):
    """Получение товаров с наибольшим процентом скидки"""
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute("""SELECT * FROM sales ORDER BY percent_sale DESC"""))


def low_prices(filename):
    """Получение товаров с наименьшей ценой"""
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute("""SELECT * FROM sales ORDER BY price_promo_min"""))


def search_by_text(filename, request: str):
    """Получение товаров по текстовому запросу"""
    request_lower = request.lower()
    request_upper = request.upper()
    request_title = request.title()

    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute(f"""SELECT * FROM sales
        WHERE (name LIKE '%{request} %') or (name LIKE '%{request_lower} %') or (name LIKE '%{request_title} %') or (name LIKE '%{request_upper} %')
        ORDER BY percent_sale DESC"""))


def reformat_date(date, is_begin):
    """Форматирование даты в текстовый вид"""
    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря',
    }

    date_end = date.split('-')
    day = date_end[-1]

    if day[0] == '0':
        day = day[1:]

    prefix = 'с' if is_begin else 'до'

    return f'{prefix} {day} {months.get(date_end[1])}'


def generate_text(sales: tuple, count_sales):
    """Генерация текста сообщения для вывода"""
    text = ''

    figures = {0: '🔸',
               1: '🔹'}

    counter = 0
    for sale in sales[:count_sales]:
        figure = figures.get(counter % 2)
        name = sale[1]
        percent = sale[7]
        old_price = sale[5]
        new_price = sale[6]
        date_end = sale[4]

        text += f'{figure} {name}\n{percent}% <b>|</b> <s>{old_price}</s> ➡ <b>{new_price} руб.</b>\n{date_end}\n\n'
        counter += 1

    return text


def split_into_pages(sales: tuple, step: int) -> list:
    """Разделение товаров на страницы"""
    pages = []
    page_number = 0
    last_element_index = 0
    for i in range(step, len(sales) + step, step):
        page_number += 1
        title = f'Страница {page_number}\n\n'
        main_text = generate_text(sales[last_element_index:i], step)

        pages.append(title + main_text)
        last_element_index = i

    return pages


if __name__ == '__main__':
    # with sqlite3.connect('P_MSC_S801_091122.db') as con:
    #     cur = con.cursor()
    #     sales = tuple(cur.execute("""SELECT * FROM sales"""))

    # split_into_pages(sales, 3)
    pass