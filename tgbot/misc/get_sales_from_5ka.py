# Работа с магазином Пятёрочка

import requests
import sqlite3

from tgbot.misc.work_with_text import reformat_date


def get_sales_from_one_page_5ka(page, store):
    """Получение скидок Пятёрочки с одной страницы"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://5ka.ru/special_offers',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'records_per_page': '20',
        'page': str(page),
        'store': store,
        'ordering': '',
        'price_promo__gte': '',
        'price_promo__lte': '',
        'categories': '',
        'search': '',
    }

    response = requests.get('https://5ka.ru/api/v2/special_offers/', params=params, headers=headers)

    return response.json()['results']


def get_all_sales_from_all_pages_5ka(filename, store):
    """Создание базы данных со всеми скидками Пятёрочки в указанном магазине"""
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        cur.execute("""DROP TABLE IF EXISTS sales""")
        cur.execute("""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER,
        name TEXT,
        img_link TEXT,
        date_begin TEXT,
        date_end TEXT,
        price_reg_min REAL,
        price_promo_min REAL,
        percent_sale INTEGER,
        store_name TEXT)""")

    received_sales_len = 0
    last_length = 0
    for page in range(1, 1000 + 1):
        products = get_sales_from_one_page_5ka(page, store)

        for product in products:
            price_reg_min = product.get('current_prices').get('price_reg__min')
            price_promo_min = product.get('current_prices').get('price_promo__min')
            percent_sale = int(100 - price_promo_min / price_reg_min * 100)

            date_begin = reformat_date(product.get('promo').get('date_begin'), is_begin=True)
            date_end = reformat_date(product.get('promo').get('date_end'), is_begin=False)
            product_after_process = (product.get('id'),
                                     product.get('name').strip(),
                                     product.get('img_link').strip(),
                                     date_begin.strip(),
                                     date_end.strip(),
                                     price_reg_min,
                                     price_promo_min,
                                     percent_sale,
                                     product.get('store_name').strip())

            with sqlite3.connect(filename) as con:
                cur = con.cursor()
                cur.executemany(f"""INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (product_after_process,))

        received_sales_len += len(products)

        if received_sales_len == last_length:
            break
        else:
            last_length = received_sales_len


def check_5ka_store_code(store_code):
    """Проверка существования магазина Пятёрочки по указанному коду"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://5ka.ru/special_offers',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'records_per_page': '20',
        'page': '1',
        'store': store_code,
        'ordering': '',
        'price_promo__gte': '',
        'price_promo__lte': '',
        'categories': '',
        'search': '',
    }

    response = requests.get('https://5ka.ru/api/v2/special_offers/', params=params, headers=headers)

    city = None
    if response.text.startswith('{'):
        city = response.json().get('store_address')
    return city






