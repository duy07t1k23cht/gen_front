import numpy as np
import random
import datetime
from PIL import Image, ImageDraw, ImageFont


def gen_idnumber():
    return "1 2 3 4 5 6 7 8 9"


def gen_fullname():
    return "Nguyễn Thị Một Cái Tên Dài Thiệt Là Dài"


def gen_birthday():
    start_date = datetime.date(1980, 1, 1)
    end_date = datetime.date(2004, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    date = random_date.day
    month = random_date.month
    year = random_date.year

    return ("{}/{}/{}").format(date, month, year)


def gen_hometown():
    return "Một cái nguyên quán dài thiệt là dài"


def gen_current_place():
    return "Một cái địa chỉ dài thiệt là dài"

