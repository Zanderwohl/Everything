import re
import datetime


def is_date(string):
    date = re.compile('^\\d{2,4}-\\d{1,2}-\\d{1,2}$')
    if date.match(string):
        return True
    return False


def parse_date_iso(date):
    date_list = date.split('-')
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]
    return str(year), lead_zero(month), lead_zero(day)


def layout_date_iso(year, month, day):
    return year + '-' + lead_zero(month) + '-' + lead_zero(day)


def lead_zero(number):
    if len(str(number)) == 1:
        return '0' + str(number)
    return str(number)


def now_tuple():
    now = datetime.datetime.now()
    expected_date = str(now.year), lead_zero(now.month), lead_zero(now.day)
    return expected_date


def now_string():
    return layout_date_iso(*now_tuple())
