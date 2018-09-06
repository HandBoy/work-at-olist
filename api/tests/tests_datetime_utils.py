from datetime import datetime

from django.test import TestCase

from api.datetime_utils import get_previous_month

from api.exceptions import MonthInvalidAPIError


class PreviousMonthTest(TestCase):
    def test_when_month_is_none(self):
        month = datetime.now().month-1
        year = datetime.now().year
        self.assertListEqual(get_previous_month(None, year), [month, year])

    def test_none_month_none_year(self):
        month = datetime.now().month-1
        year = datetime.now().year
        self.assertListEqual(get_previous_month(None, None), [month, year])

    def test_actual_month_actual_year(self):
        month = datetime.now().month
        year = datetime.now().year
        self.assertListEqual(get_previous_month(month, year), [month-1, year])

    def test_actual_month_next_year(self):
        month = datetime.now().month
        year = datetime.now().year+1
        self.assertListEqual(get_previous_month(month, year), 
                             [month-1, year-1])

    def test_actual_month_last_year(self):
        month = datetime.now().month
        year = datetime.now().year-1
        self.assertListEqual(get_previous_month(month, year), [month, year])

    def test_next_month_actual_year(self):
        month = datetime.now().month+1
        year = datetime.now().year
        self.assertListEqual(get_previous_month(month, year), [month-2, year])

    def test_next_month_next_year(self):
        month = datetime.now().month+1
        year = datetime.now().year+1
        self.assertListEqual(get_previous_month(month, year),
                             [month-2, year-1])

    def test_next_month_last_year(self):
        month = datetime.now().month+1
        year = datetime.now().year-1
        self.assertListEqual(get_previous_month(month, year), [month, year])

    def test_last_month_actual_year(self):
        month = datetime.now().month-1
        year = datetime.now().year
        self.assertListEqual(get_previous_month(month, year), [month, year])

    def test_month_invalid(self):
        with self.assertRaises(MonthInvalidAPIError):
            get_previous_month(13, 2018)

    def test_month_changed_by_year(self):
        with self.assertRaises(MonthInvalidAPIError):
            get_previous_month(2018)
