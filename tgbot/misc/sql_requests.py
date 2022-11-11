# SQL запросы

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
        WHERE (name LIKE '%{request} %')
        or (name LIKE '%{request_lower} %')
        or (name LIKE '%{request_title} %')
        or (name LIKE '%{request_upper} %')
        ORDER BY percent_sale DESC"""))


def add_user_to_db(user_id, full_name, user_name):

    user_data = (user_id, full_name, user_name)
    with sqlite3.connect('data/users.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                full_name TEXT,
                username TEXT)""")

        all_users = cur.execute("""SELECT * FROM users""")

        if user_data not in all_users:
            cur.execute("""INSERT INTO users VALUES (?, ?, ?)""", user_data)
