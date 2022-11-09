def get_page(sales, page: int = 1):
    page_index = page - 1
    return sales[page_index]