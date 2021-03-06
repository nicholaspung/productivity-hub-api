import calendar
from datetime import date, timedelta


def get_date(data):
    if 'date' in data:
        request_date = data["date"]
        return date(int(request_date[:4]), int(
            request_date[5:7]), int(request_date[-2:]))

    return date.today()


def get_week_range(iso_calendar):
    iso_calendar_year = iso_calendar[0]
    iso_calendar_week = iso_calendar[1]
    if iso_calendar[2] == 7:
        iso_calendar_week += 1
    if iso_calendar_week == 54:
        iso_calendar_year += 1
        iso_calendar_week = 1
    beginning_of_week = date.fromisocalendar(
        iso_calendar_year, iso_calendar_week, 1)
    return (beginning_of_week - timedelta(days=1), beginning_of_week + timedelta(days=5))


def get_month_range(year, month):
    return (date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1]))


def get_year_range(year):
    return (date(year, 1, 1), date(year, 12, 31))
