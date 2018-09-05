from django.test import TestCase
from django.core.exceptions import ValidationError
from calls.models import (CallStart, Call, Charge)
from datetime import time


class CallStartTests(TestCase):

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

    def test_no_source_and_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)

        with self.assertRaises(ValidationError):
            CallStart.objects.create(call_id=call, source='', destination='')

    def test_no_source_and_invalid_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='',
                destination='999999999999')

    def test_no_destination_and_invalid_source_phone_number(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='999999999999',
                destination='')

    def test_phone_number_format_more_digits(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='999999999999',
                destination='999999999999')

    def test_phone_number_format_less_digits(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='99999',
                destination='999999')

    def test_source_eguals_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='84998182665')

    def test_valid_phone_call(self):
        call = Call.objects.create(charge=self.charge)
        call_start = CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='84998182660')

        self.assertIsNotNone(call_start)
        self.assertIsInstance(call_start, CallStart)
