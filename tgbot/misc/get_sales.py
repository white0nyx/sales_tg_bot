import requests
import sqlite3


def get_stores():
    pass


def get_sales_from_one_page(page, store):
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


def get_all_sales_from_all_pages(filename, store):
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        cur.execute("""DROP TABLE IF EXISTS sales""")
        cur.execute("""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER,
        name TEXT,
        img_link TEXT,
        promo_id INTEGER,
        date_begin TEXT,
        date_end TEXT,
        price_reg_min REAL,
        price_promo_min REAL,
        percent_sale REAL,
        store_name TEXT)""")

    received_sales_len = 0
    last_length = 0
    for page in range(1, 1000 + 1):
        products = get_sales_from_one_page(page, store)

        for product in products:
            price_reg_min = product.get('current_prices').get('price_reg__min')
            price_promo_min = product.get('current_prices').get('price_promo__min')
            percent_sale = round(100 - price_promo_min / price_reg_min * 100, 2)

            product_after_process = (product.get('id'),
                                     product.get('name'),
                                     product.get('img_link'),
                                     product.get('promo').get('id'),
                                     product.get('promo').get('date_begin'),
                                     product.get('promo').get('date_end'),
                                     price_reg_min,
                                     price_promo_min,
                                     percent_sale,
                                     product.get('store_name'))

            with sqlite3.connect(filename) as con:
                cur = con.cursor()
                cur.executemany(f"""INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (product_after_process,))

        received_sales_len += len(products)

        if received_sales_len == last_length:
            break
        else:
            last_length = received_sales_len


def best_sales(filename):
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute("""SELECT * FROM sales ORDER BY percent_sale DESC"""))


def low_prices(filename):
    with sqlite3.connect(filename) as con:
        cur = con.cursor()
        return tuple(cur.execute("""SELECT * FROM sales ORDER BY price_promo_min"""))

