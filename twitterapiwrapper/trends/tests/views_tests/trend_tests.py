from rest_framework.test import APITestCase
from rest_framework import status


from ... import models


class TrendAPITestCase(APITestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.trend_data = {
            'name': 'api_created',
            'tweet_volume': 102,
            'url': 'https://domain.com/api/created/ok'
        }

    def test_create_account(self):
        """
        Ensure we can create a new instance of Trend.
        """
        url = '/trends/'
        response = self.client.post(url, self.trend_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Trend.objects.count(), 1)
        instance = models.Trend.objects.get()
        self.assertEqual(instance.name, 'api_created')
        self.assertEqual(instance.tweet_volume, 102)
        self.assertEqual(instance.url, 'https://domain.com/api/created/ok')
