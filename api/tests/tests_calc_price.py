from datetime import datetime, time

import pytz
from django.test import TestCase

from calls.models import Charge

from api.calc_price import CalcPrice

# Create your tests here.


class CalculatePriceTest(TestCase):
    def setUp(self):
        Charge.objects.get_or_create(
            name='Standard time call',
            standard_time_start=time(6, 0, 0),
            standard_time_end=time(22, 0, 0),
            standing_time_charge=0.36,
            standing_time_minute=0.09,
            reduced_time_start=time(22, 0, 0),
            reduced_time_end=time(6, 0, 0),
            reduced_time_charge=0.36,
            reduced_time_minute=0.09
            )

        self.charge = Charge.objects.get(id=1)
    # Start hour of phone call == Finish hour of phone call

    def test_when_call_is_tariff_standard_and_same_hour(self):
        start_call = datetime(2018, 6, 18, 10, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 10, 35, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 3.51)

    def test_when_call_is_reduced_tariff_and_same_hour(self):
        start_call = datetime(2018, 6, 18, 23, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 23, 35, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 0.36)

    # Start of phone call <= Fnish of phone call

    def test_when_tariff_standard_end_same_day(self):
        start_call = datetime(2018, 6, 18, 10, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 11, 13, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 3.06)

    def test_tariff_standard_end_same_day_later(self):
        start_call = datetime(2018, 6, 18, 14, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 15, 13, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 3.06)

    def test_tariff_standard_end_next_day(self):
        start_call = datetime(2018, 6, 18, 14, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 15, 13, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 89.46)

    def test_start_lt_start_standard_end_gt_start_standard(self):
        start_call = datetime(2018, 6, 18, 4, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 7, 17, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 7.29)

    def test_start_lt_start_standard_end_gt_start_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 4, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 7, 17, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 93.69)

    def test_start_lt_start_standard_end_gt_end_standard(self):
        start_call = datetime(2018, 6, 18, 5, 23, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 23, 42, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 86.76)

    def test_start_lt_start_standard_end_gt_end_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 5, 23, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 23, 42, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 173.16)

    def test_start_and_end_gt_start_and_end_standart(self): 
        start_call = datetime(2018, 6, 18, 20, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 23, 13, 43, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 7.2)

    def test_start_and_end_gt_start_and_end_standart_next_day(self):
        start_call = datetime(2018, 6, 18, 20, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 23, 13, 43, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 93.6)

    def test_start_lt_start_standard_end_lt_start_standard(self):
        start_call = datetime(2018, 6, 18, 3, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 5, 33, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 0.36)

    def test_test_start_lt_start_standard_end_lt_start_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 3, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 5, 33, 58, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 86.76)

    def test_test_reduced_tariff_after_standard(self):
        start_call = datetime(2018, 6, 18, 22, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 23, 5, 43, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 0.36)

    def test_test_reduced_tariff_after_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 22, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 23, 5, 43, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 86.76)

    # Start of phone call > Fnish of phone call

    def test_start_gt_end_standard_end_gt_start_standard(self):
        start_call = datetime(2018, 6, 18, 23, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 8, 0, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 11.16)

    def test_start_gt_end_standard_end_gt_start_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 23, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 20, 8, 0, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 97.56)

    def test_on_intervals_within_the_standard(self):
        start_call = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 8, 0, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 21.96)

    def test_on_intervals_within_the_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 20, 8, 0, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 108.36)

    def test_one_intervals_within_the_standard(self):
        start_call = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 19, 5, 0, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 11.16)

    def test_test_one_intervals_within_the_standard_next_day(self):
        start_call = datetime(2018, 6, 18, 20, 0, 0, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 20, 5, 0, 0, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 97.56)

    def test_reduced_tariff_after_standard_across_day(self):
        start_call = datetime(2018, 6, 18, 22, 43, 58, tzinfo=pytz.utc)
        end_call = datetime(2018, 6, 18, 5, 35, 43, tzinfo=pytz.utc)
        calc = CalcPrice(start_call, end_call, self.charge)
        self.assertEqual(calc.calculate_price(), 0.36)
