import time
from datetime import timedelta

SECONDS_IN_DAY = 86400


def convert_to_seconds_from_midnight(s: str):
    t = time.strptime(s, '%H:%M:%S')
    t1_timedelta = timedelta(
        hours=t.tm_hour,
        minutes=t.tm_min,
        seconds=t.tm_sec)

    return t1_timedelta.seconds


def convert_to_cents(price_string: str):
    if len(price_string.split('.')[1]) != 2:
        raise ValueError(f'Price str {price_string} is not in a correct format')
    formatted_price = price_string.replace('.', '').replace(',', '')
    return int(formatted_price)


def subtract_dates_in_seconds(t_minuend: int, t_subtrahend: int):
    """
    Returns (t_minuend - t_subtrahend) mod (amount of seconds in day)
    """

    return (t_minuend - t_subtrahend) % SECONDS_IN_DAY
