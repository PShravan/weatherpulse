import pytz
from datetime import datetime


def convert_ist_to_utc(ist_datetime_str: str) -> datetime:
    """
    Converts a datetime string from IST to UTC.

    :param ist_datetime_str: A string representing a datetime in 'YYYY-MM-DD HH:MM' format in IST.
    :return: A datetime object in UTC.
    """
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_time_naive = datetime.strptime(ist_datetime_str, '%Y-%m-%d %H:%M')

    ist_time = ist_tz.localize(ist_time_naive)

    utc_time = ist_time.astimezone(pytz.utc)

    return utc_time


def convert_celsius_to_fahreheit(celsius):
    return 1.8 * float(celsius) + 32


def convert_kmph_to_mph(kmph):
    return kmph * 0.621371
