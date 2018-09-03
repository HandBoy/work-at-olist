from datetime import time

from django.test import TestCase

from calls.models import RatePlans


# Create your tests here.


class TesteCreateCallViewSet(TestCase):
    def test_not_allowed_get_method(self):
        response = self.client.get(
            '/api/startcall/',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_put_method(self):
        response = self.client.put(
            '/api/startcall/',
            content_type='application/json',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_delete_method(self):
        response = self.client.delete(
            '/api/startcall/',
            content_type='application/json',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_send_invalid_data_empty(self):
        invalid_data = '{}'
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_invalid_data_only_source(self):
        invalid_data = '{"source": "84998182665"}'
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_invalid_data_fields_unknown(self):
        invalid_data = ('{"fieldErr": "84998182665",'
                        + '"fieldErr": "8499818230"}')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_both_bigger(self):
        invalid_data = ('{'
                        + '"source": "84998182665222",'
                        + '"destination": "8499818230222" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_both_little(self):
        invalid_data = ('{'
                        + '"source": "8499818",'
                        + '"destination": "8499818" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_source_little_destination_bigger(self):
        invalid_data = ('{'
                        + '"source": "8499818",'
                        + '"destination": "8499818230222" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_source_bigger_destination_little(self):
        invalid_data = ('{'
                        + '"source": "84998182665222",'
                        + '"destination": "8499818" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_iguals_source_and_destination(self):
        invalid_data = ('{'
                        + '"source": "84998182665",'
                        + '"destination": "84998182665" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_valid_phone_number(self):
        valid_data = ('{'
                      + '"source": "84998182665",'
                      + '"destination": "84998182635" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=valid_data,
            follow=True)
        self.assertEqual(response.status_code, 201)


class EndCallViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        RatePlans.objects.get_or_create(
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

    def test_not_allowed_get_method(self):
        response = self.client.get(
            '/api/endcall/',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_post_method(self):
        response = self.client.post(
            '/api/endcall/',
            content_type='application/json',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_delete_method(self):
        response = self.client.delete(
            '/api/endcall/',
            content_type='application/json',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_send_invalid_data_empty(self):
        invalid_data = '{}'
        response = self.client.put(
            '/api/endcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_invalid_field_and_id(self):
        invalid_data = '{"id": 999999}'
        response = self.client.put(
            '/api/endcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_valid_id(self):
        valid_data = ('{'
                      + '"source": "84998182665",'
                      + '"destination": "84998182635" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=valid_data,
            follow=True)

        call_id = response.data['call_id']

        valid_data = ("{\"call_id\": %d }" % call_id)

        response = self.client.put(
            '/api/endcall/',
            content_type='application/json',
            data=valid_data,
            follow=True)
        self.assertEqual(response.status_code, 201)


class MonthlyBilling(TestCase):
    def test_no_phone_year_and_month(self):
        response = self.client.put(
            '/api/billing/',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_little_phone_and_no_year_and_month(self):
        response = self.client.put(
            '/api/billing/123',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_little_phone_and_year_and_no_month(self):
        response = self.client.put(
            '/api/billing/123/123',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_little_phone_month(self):
        response = self.client.put(
            '/api/billing/123/2018/123',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_little_phone_month_with_year_and_month(self):
        response = self.client.put(
            '/api/billing/123/2018/08',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_bigger_phone_and_no_year_and_month(self):
        response = self.client.put(
            '/api/billing/123123123123',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_bigger_phone_year_and_no_month(self):
        response = self.client.put(
            '/api/billing/123123123123/123',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_bigger_phone_month(self):
        response = self.client.put(
            '/api/billing/123123123123/2018/123',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_bigger_phone_month_with_year_and_month(self):
        response = self.client.put(
            '/api/billing/123123123123/2018/08',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_valid_phone_year_and_month(self):
        response = self.client.put(
            '/api/billing/84998182665/2018/08',
            follow=True)
        self.assertEqual(response.status_code, 200)

    def test_no_phone_calls_in_month(self):
        response = self.client.put(
            '/api/billing/84998182665/2018/05',
            follow=True)
        message = "No phone calls in 05 2018"
        message_response = response.data["Msg"]
        self.assertEqual(message_response, message)
