from datetime import datetime


def cut_price(price):
    price = str(price).strip()
    if '.' in price:
        price = price.split('.')[0] + '.' + price.split('.')[1][:2]
    return price

def is_valid_date(date_str):
    formats = ["%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d"]
    if date_str:
        for fmt in formats:
            try:
                dt_time = datetime.strptime(date_str, fmt)
                return dt_time
            except ValueError:
                continue
    return False


def is_valid_price(price):
    try:
        float(price)
        return True
    except ValueError:
        return False