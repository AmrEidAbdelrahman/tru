from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey

class NationalIDValidatorAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('validate-id')
        self.api_key, self.key = APIKey.objects.create_key(name="test-key")
        self.auth_header = {'HTTP_AUTHORIZATION': f'Api-Key {self.key}'}

    def test_valid_national_id(self):
        data = {"national_id": "29901011234567"}  # 1999-01-01, valid format
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('birthdate', response.data)
        self.assertIn('governorate_code', response.data)
        self.assertIn('gender', response.data)

    def test_invalid_national_id_length(self):
        data = {"national_id": "12345"}
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_national_id_non_numeric(self):
        data = {"national_id": "abcdefghijklmno"}
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_missing_api_key(self):
        data = {"national_id": "29901011234567"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_api_key(self):
        data = {"national_id": "29901011234567"}
        response = self.client.post(self.url, data, format='json', HTTP_AUTHORIZATION='Api-Key invalidkey')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
