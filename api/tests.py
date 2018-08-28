from datetime import datetime, time

import pytz
from django.test import TestCase

from calls.models import RatePlans

from .utils import calculate_price, get_correct_date

# Create your tests here.

class TesteGetCorrectDate(TestCase):
    def test_none_month(self):
        month = datetime.now().month-1
        year = datetime.now().year
        self.assertListEqual(get_correct_date(None, year), [month, year])
    
    def test_none_month_none_year(self):
        month = datetime.now().month-1
        year = datetime.now().year
        self.assertListEqual(get_correct_date(None, None), [month, year])

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


class TesteGetCalculatePrice(TestCase):

    def setUp(self):        
        RatePlans.objects.get_or_create(
            name = 'Standard time call',
            standard_time_start = time(6,0,0),
            standard_time_end   = time(22,0,0),
            standing_time_charge = 0.36,
            standing_time_minute = 0.09,
            reduced_time_start = time(22,0,0),
            reduced_time_end = time(6,0,0),
            reduced_time_charge = 0.36,
            reduced_time_minute = 0.09
            )
    #Start one day == Fnish next day
    #Start < Fnish

    def test_tariff_standard_end_same_day(self): # 1
        start_call  = datetime(2018, 6, 18, 10, 43, 58)
        end_call    = datetime(2018, 6, 18, 11, 13, 58)
        self.assertEqual(calculate_price(start_call, end_call), 3.06)

    def test_tariff_standard_end_same_day_later(self): # 1
        start_call  = datetime(2018, 6, 18, 14, 43, 58)
        end_call    = datetime(2018, 6, 18, 15, 13, 58)
        self.assertEqual(calculate_price(start_call, end_call), 3.06)

    def test_tariff_standard_end_next_day(self): # 1
        start_call  = datetime(2018, 6, 18, 14, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 15, 13, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 89.46)

    def test_start_lt_start_standard_end_gt_start_standard(self): #4
        start_call  = datetime(2018, 6, 18, 4, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 18, 7, 17, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 7.29)
    
    def test_start_lt_start_standard_end_gt_start_standard_next_day(self): #4
        start_call  = datetime(2018, 6, 18, 4, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 7, 17, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 93.69)

    def test_start_lt_start_standard_end_gt_end_standard(self): #6
        start_call  = datetime(2018, 6, 18, 5, 23, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 18, 23, 42, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 86.76)
    
    def test_start_lt_start_standard_end_gt_end_standard_next_day(self): #6
        start_call  = datetime(2018, 6, 18, 5, 23, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 23, 42, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 173.16)   

    def test_start_and_end_gt_start_and_end_standart(self): #5
        start_call  = datetime(2018, 6, 18, 20, 43, 58)
        end_call    = datetime(2018, 6, 18, 23, 13, 43)
        self.assertEqual(calculate_price(start_call, end_call), 7.2)

    def test_start_and_end_gt_start_and_end_standart_next_day(self): #5
        start_call  = datetime(2018, 6, 18, 20, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 23, 13, 43, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 93.6) 

    def test_start_lt_start_standard_end_lt_start_standard(self): #2
        start_call  = datetime(2018, 6, 18, 3, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 18, 5, 33, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 0.36)

    def test_start_lt_start_standard_end_lt_start_standard_next_day(self): #2
        start_call  = datetime(2018, 6, 18, 3, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 5, 33, 58, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 86.76)

    def test_reduced_tariff_after_standard(self): # 3
        start_call  = datetime(2018, 6, 18, 22, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 18, 23, 5, 43, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 0.36)

    def test_reduced_tariff_after_standard_next_day(self): #3
        start_call  = datetime(2018, 6, 18, 22, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 23, 5, 43, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 86.76)

    #Start > Fnish

    def test_start_gt_end_standard_end_gt_start_standard(self): #7
        start_call  = datetime(2018, 6, 18, 23, 0, 0, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 8, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 11.16)

    def test_start_gt_end_standard_end_gt_start_standard_next_day(self): #7
        start_call  = datetime(2018, 6, 18, 23, 0, 0, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 20, 8, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 97.56)

    def test_on_intervals_within_the_standard(self): #9
        start_call  = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 8, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 21.96)

    def test_on_intervals_within_the_standard_next_day(self): #9
        start_call  = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 20, 8, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 108.36)

    def test_one_intervals_within_the_standard(self): #8
        start_call  = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 19, 5, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 11.16)

    def test_one_intervals_within_the_standard_next_day(self): #8
        start_call  = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 20, 5, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 97.56) 
    
    def test_reduced_tariff_after_standard_across_day(self): # 3
        start_call  = datetime(2018, 6, 18, 22, 43, 58, tzinfo=pytz.utc)
        end_call    = datetime(2018, 6, 18, 5, 35, 43, tzinfo=pytz.utc)
        self.assertEqual(calculate_price(start_call, end_call), 0.36)
