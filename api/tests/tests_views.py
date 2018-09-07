from datetime import time

from django.test import TestCase

from calls.models import Charge

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

# Create your tests here.


class CreateCallViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 's3cr3tp@ss',
            'email': 'teste@email.com',
            'is_superuser': 1}
        cls.user = User.objects.create_user(**cls.credentials)

        cls.token = Token.objects.create(user=cls.user)

    def test_not_allowed_get_method(self):
        response = self.client.get(
            '/api/call/start/',
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_put_method(self):
        response = self.client.put(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_delete_method(self):
        response = self.client.delete(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_send_invalid_data_empty(self):
        invalid_data = '{}'
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_invalid_data_only_source(self):
        invalid_data = '{"source": "84998182665"}'
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_invalid_data_fields_unknown(self):
        invalid_data = ('{"fieldErr": "84998182665",'
                        + '"fieldErr": "8499818230"}')

        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_both_bigger(self):
        invalid_data = ('{'
                        + '"source": "84998182665222",'
                        + '"destination": "8499818230222" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_both_little(self):
        invalid_data = ('{'
                        + '"source": "8499818",'
                        + '"destination": "8499818" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_source_little_destination_bigger(self):
        invalid_data = ('{'
                        + '"source": "8499818",'
                        + '"destination": "8499818230222" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_source_bigger_destination_little(self):
        invalid_data = ('{'
                        + '"source": "8499818230222",'
                        + '"destination": "8499818" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_number_iguals_source_and_destination(self):
        invalid_data = ('{'
                        + '"source": "84998182665",'
                        + '"destination": "84998182665" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_valid_phone_number(self):
        valid_data = ('{'
                      + '"source": "84998182665",'
                      + '"destination": "84998182635" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=valid_data,
            follow=True)
        self.assertEqual(response.status_code, 201)


class EndCallViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 's3cr3tp@ss',
            'email': 'teste@email.com',
            'is_superuser': 1}
        cls.user = User.objects.create_user(**cls.credentials)

        cls.token = Token.objects.create(user=cls.user)

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

    def test_not_allowed_get_method(self):
        response = self.client.get(
            '/api/call/0/end/',

            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_post_method(self):
        response = self.client.post(
            '/api/call/0/end/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_delete_method(self):
        response = self.client.delete(
            '/api/call/0/end/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        self.assertEqual(response.status_code, 405)

    def test_send_invalid_data_empty(self):
        response = self.client.put(
            '/api/call/end/',
            content_type='application/json',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_send_invalid_field_and_id(self):
        response = self.client.put(
            '/api/call/999999/end/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_end_call_twice(self):
        valid_data = ('{'
                      + '"source": "84998182665",'
                      + '"destination": "84998182635" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=valid_data,
            follow=True)
        call_id = response.data['call_id']

        self.client.put(
            ("/api/call/%s/end/" % (call_id)),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        
        response = self.client.put(
            ("/api/call/%s/end/" % (call_id)),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_send_valid_id(self):
        valid_data = ('{'
                      + '"source": "84998182665",'
                      + '"destination": "84998182635" }')
        response = self.client.post(
            '/api/call/start/',
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=valid_data,
            follow=True)
        call_id = response.data['call_id']

        valid_data = ("{\"call_id\": %d }" % call_id)

        response = self.client.put(
            ("/api/call/%s/end/" % (call_id)),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token %s" % self.token,
            data=valid_data,
            follow=True)
        print(response.data)
        self.assertEqual(response.status_code, 201)


class MonthlyBilling(TestCase):
    def test_no_phone_year_and_month(self):
        response = self.client.get(
            '/api/bills/',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_little_phone_and_no_year_and_month(self):
        response = self.client.get(
            '/api/bills/123',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_little_phone_and_year_and_no_month(self):
        response = self.client.get(
            '/api/bills/123/123',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_little_phone_month(self):
        response = self.client.get(
            '/api/bills/123/&year=2018&month=123',
            follow=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_little_phone_month_with_year_and_month(self):
        response = self.client.get(
            '/api/bills/123/?year=2018&month=08',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_bigger_phone_and_no_year_and_month(self):
        response = self.client.get(
            '/api/bills/123123123123',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_bigger_phone_year_and_no_month(self):
        response = self.client.get(
            '/api/bills/123123123123/?year=123',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_bigger_phone_month(self):
        response = self.client.get(
            '/api/bills/123123123123/?year=2018&month=123',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_bigger_phone_month_with_year_and_month(self):
        response = self.client.get(
            '/api/bills/123123123123/?year=2018&month=08',
            follow=True)
        self.assertEqual(response.status_code, 400)

    def test_valid_phone_year_and_month(self):
        response = self.client.get(
            '/api/bills/84998182665/?year=2018&month=08',
            follow=True)
        self.assertEqual(response.status_code, 200)

    def test_no_phone_calls_in_month(self):
        response = self.client.get(
            '/api/bills/84998182635/?year=2018&month=05',
            follow=True)
        message = "No phone calls in 5 2018"
        message_response = response.data["Msg"]
        self.assertEqual(message_response, message)
