def get_page(sales, page: int = 1):
    """Получение содержания страницы по её порядковому номеру"""
    page_index = page - 1
    return sales[page_index]