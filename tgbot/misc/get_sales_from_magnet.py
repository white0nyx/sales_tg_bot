import requests
from bs4 import BeautifulSoup
import sqlite3


def get_sales_from_one_page_magnet(filename, store):
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

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://magnit.ru',
        'Referer': 'https://magnit.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    cookies = {
        'mg_geo_id': f'{store}'
    }

    collected = 0
    count_discounts = None
    for page in range(1, 10_000):

        data = {
            'page': f'{page}',
        }

        response = requests.post('https://magnit.ru/promo/', cookies=cookies, headers=headers, data=data)

        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('a', 'card-sale_catalogue')

        if not count_discounts:
            count_discounts = int(soup.find(class_='js-сatalogue__header-text сatalogue__header-text').text.split()[1])

        for product in products:
            try:
                texts = product.find_all('p')
                if len(texts) < 3:
                    continue

                name = texts[2].text.strip()
                part_of_link = product.find("img").get('data-src').strip()
                img_link = f'https://magnit.ru{part_of_link}'
                date_begin, date_end = product.find_all('div')[-2].text.strip().split('\n')
                date_end = date_end.replace('  ', ' ')

                if not product.find('span', 'label__price-integer'):
                    return

                old_price = product.find(class_='label__price label__price_old')
                price_reg_min = f"{old_price.find(class_='label__price-integer').text}.{old_price.find(class_='label__price-decimal').text}"

                discount_price = product.find(class_='label__price label__price_new')
                price_promo_min = f"{discount_price.find(class_='label__price-integer').text}.{discount_price.find(class_='label__price-decimal').text}"

                try:
                    percent_sale = int(
                        product.find(class_='label label_sm label_magnit card-sale__discount').text[1:-1])
                except AttributeError:
                    percent_sale = int((float(price_reg_min) - float(price_promo_min)) / float(price_reg_min) * 100)
                product_after_process = ('NULL',
                                         name,
                                         img_link,
                                         date_begin,
                                         date_end,
                                         price_reg_min,
                                         price_promo_min,
                                         percent_sale,
                                         'NULL')

                with sqlite3.connect(filename) as con:
                    cur = con.cursor()
                    cur.executemany(f"""INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (product_after_process,))

                collected += 1

            except AttributeError:
                pass


def check_magnet_city_code(city_code):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://magnit.ru',
        'Referer': 'https://magnit.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    data = {
        'page': '1',
    }

    response = requests.post('https://magnit.ru/promo/', cookies=cookies, headers=headers, data=data)

    if 'TypeError' in response.text:
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    city = soup.find('span', class_='header__contacts-text').text
    return city


if __name__ == '__main__':
    print(check_magnet_city_code('1398'))
