import sqlite3


def best_sales(filename):
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute("""SELECT * FROM sales ORDER BY percent_sale DESC"""))


def low_prices(filename):
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute("""SELECT * FROM sales ORDER BY price_promo_min"""))


def search_by_text(filename, request: str):
    request_lower = request.lower()
    request_upper = request.upper()
    request_title = request.title()

    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute(f"""SELECT * FROM sales
        WHERE (name LIKE '%{request} %') or (name LIKE '%{request_lower} %') or (name LIKE '%{request_title} %') or (name LIKE '%{request_upper} %')
        ORDER BY percent_sale DESC"""))


def reformat_date(date, is_begin):
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
