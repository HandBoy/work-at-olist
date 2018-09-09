from datetime import datetime

from django.test import TestCase

from api.datetime_utils import (
                                get_previous_month, total_minutes,
                                time_difference)

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


class TotalMinutesTest(TestCase):
    def test_sum_minutes(self):
        now = datetime.now()
        then = now.replace(hour=now.hour+1)
        minutes_add = 15
        self.assertEqual(total_minutes(then-now)+minutes_add, 75)


class TimeDifferenceTest(TestCase):
    def test_one_hour_of_difference(self):
        now = datetime.now().time()
        then = now.replace(hour=now.hour+1)

        self.assertEqual(time_difference(now, then), 60)

    def test_two_hour_of_difference(self):
        now = datetime.now().time()
        then = now.replace(hour=now.hour+2)

        self.assertEqual(time_difference(now, then), 120)

    def test_start_one_day_end_another(self):
        start = datetime(2018, 9, 11, 22, 0, 0)
        then = datetime(2018, 9, 12, 6, 0, 0)

        self.assertEqual(time_difference(start.time(), then.time()), 480)
