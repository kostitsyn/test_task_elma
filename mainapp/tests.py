from rest_framework import status
from rest_framework.test import APISimpleTestCase


class TestBaseApiView(APISimpleTestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/'
        self.request_body = {
            "urls": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://python.org", "query": "python"}
            ],
            "maxTimeout": 3000
        }
        self.success_status = 'ok'
        self.error_status = 'error'

    def test_check_success_status_code(self):
        response = self.client.post(self.url, self.request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_error_status_code(self):
        wrong_request_body = {
            "eggs": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://python.org", "query": "python"}
            ],
            "maxTimeout": 3000
        }
        response = self.client.post(self.url, wrong_request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_status(self):
        response = self.client.post(self.url, self.request_body, format='json')
        self.assertIn(response.data['urls'][0]['status'], (self.success_status, self.error_status))

    def test_check_urls_count(self):
        request_count = len(self.request_body['urls'])
        response = self.client.post(self.url, self.request_body, format='json')
        self.assertEqual(request_count, len(response.data['urls']))

    def test_max_timeout_is_null(self):
        null_timeout_request_body = dict(self.request_body)
        null_timeout_request_body['maxTimeout'] = 0
        response = self.client.post(self.url, null_timeout_request_body, format='json')
        self.assertEqual(response.data['urls'][0].get('count'), None)
        self.assertEqual(response.data['urls'][0]['status'], self.error_status)
