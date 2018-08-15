from django.test import TestCase
from .utils import calculate_price, get_correct_date
from datetime import datetime
# Create your tests here.


class TesteGetCorrectDate(TestCase):
    def test_actual_month_actual_year(self):
        month = datetime.now().month
        year = datetime.now().year
        self.assertListEqual(get_correct_date(month, year), [month-1, year])

    def test_actual_month_next_year(self):
        month = datetime.now().month
        year = datetime.now().year+1
        self.assertListEqual(get_correct_date(month, year), [month-1, year-1])

    def test_actual_month_last_year(self):
        month = datetime.now().month
        year = datetime.now().year-1
        self.assertListEqual(get_correct_date(month, year), [month, year])

    def test_next_month_actual_year(self):
        month = datetime.now().month+1
        year = datetime.now().year
        self.assertListEqual(get_correct_date(month, year), [month-2, year])
    
    def test_next_month_next_year(self):
        month = datetime.now().month+1
        year = datetime.now().year+1
        self.assertListEqual(get_correct_date(month, year), [month-2, year-1])

    def test_next_month_last_year(self):
        month = datetime.now().month+1
        year = datetime.now().year-1
        self.assertListEqual(get_correct_date(month, year), [month, year])

    def test_last_month_actual_year(self):
        month = datetime.now().month-1
        year = datetime.now().year
        self.assertListEqual(get_correct_date(month, year), [month, year])

