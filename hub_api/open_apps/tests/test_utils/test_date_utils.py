from datetime import date

from django.test import TestCase
from open_apps.utils import date_utils


class DateUtilTestCase(TestCase):
    def test_get_date(self):
        data = {}
        response = date_utils.get_date(data)
        self.assertEqual(response, date.today())

    def test_get_week_range(self):
        date1 = date_utils.get_date({'date': '2020-05-14'})
        date1 = date1.isocalendar()
        response = date_utils.get_week_range(date1)
        self.assertEqual(response[0], date(2020, 5, 10))
        self.assertEqual(response[1], date(2020, 5, 16))

        date2 = date_utils.get_date({'date': '2020-12-28'})
        date2 = date2.isocalendar()
        response = date_utils.get_week_range(date2)
        self.assertEqual(response[0], date(2020, 12, 27))
        self.assertEqual(response[1], date(2021, 1, 2))

        date3 = date_utils.get_date({'date': '2021-01-03'})
        date3 = date3.isocalendar()
        response = date_utils.get_week_range(date3)
        self.assertEqual(response[0], date(2021, 1, 3))
        self.assertEqual(response[1], date(2021, 1, 9))

        date4 = date_utils.get_date({'date': '2021-01-31'})
        date4 = date4.isocalendar()
        response = date_utils.get_week_range(date4)
        self.assertEqual(response[0], date(2021, 1, 31))
        self.assertEqual(response[1], date(2021, 2, 6))

    def test_get_month_range(self):
        year = 2020
        month = 12
        response = date_utils.get_month_range(year, month)
        self.assertEqual(response[0], date(year, month, 1))
        self.assertEqual(response[1], date(year, month, 31))

    def test_get_year_range(self):
        year = 2020
        response = date_utils.get_year_range(year)
        self.assertEqual(response[0], date(year, 1, 1))
        self.assertEqual(response[1], date(year, 12, 31))
