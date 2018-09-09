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

    def test_none_source_and_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)

        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                                    call_id=call,
                                    source=None,
                                    destination=None)

    def test_none_source_phone_number(self):
        call = Call.objects.create(charge=self.charge)

        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                                    call_id=call,
                                    source=None,
                                    destination='84998182665')

    def test_none_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)

        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                                    call_id=call,
                                    source='84998182665',
                                    destination=None)

    def test_no_source_and_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)

        with self.assertRaises(ValidationError):
            CallStart.objects.create(call_id=call)

    def test_valid_source_and_bigger_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='99999999999999')

    def test_valid_destination_and_invalid_source_phone_number(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='999999999999',
                destination='84998182665')

    def test_phone_number_format_more_digits(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='999999999999',
                destination='999999999998')

    def test_phone_number_format_less_digits(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='99999',
                destination='999993')

    def test_source_eguals_destination_phone_number(self):
        call = Call.objects.create(charge=self.charge)
        with self.assertRaises(ValidationError):
            CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='84998182665')

    def test_is_not_none_phone_call(self):
        call = Call.objects.create(charge=self.charge)
        call_start = CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='84998182660')

        self.assertIsNotNone(call_start)

    def test_is_instance_call_start(self):
        call = Call.objects.create(charge=self.charge)
        call_start = CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='84998182660')
        self.assertIsInstance(call_start, CallStart)

    def test_str_call_start(self):
        call = Call.objects.create(charge=self.charge)
        call_start = CallStart.objects.create(
                call_id=call,
                source='84998182665',
                destination='84998182660')
        self.assertEqual(call_start.__str__(), call_start.source)
