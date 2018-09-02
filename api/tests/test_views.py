from django.test import TestCase

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
        invalid_data = ('{'
                        + '"source": "84998182665",'
                        + '"destination": "84998182635" }')
        response = self.client.post(
            '/api/startcall/',
            content_type='application/json',
            data=invalid_data,
            follow=True)
        self.assertEqual(response.status_code, 201)     

