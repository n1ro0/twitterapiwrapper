from django.test import TestCase
from django.shortcuts import reverse


from rest_framework.test import APIClient
from rest_framework import status


from . import models


class TrendModelTestCase(TestCase):
    """This class defines the test suite for the Trend model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.name = "Test_trend"
        self.tweet_volume = 0
        self.url = "test/url"
        self.trend = models.Trend(
            name=self.name, tweet_volume=self.tweet_volume,
            url=self.url
        )

    def test_model_can_create_a_trend(self):
        """Test the Trend model can create a trend."""
        old_count = models.Trend.objects.count()
        self.trend.save()
        new_count = models.Trend.objects.count()
        self.assertNotEqual(old_count, new_count)


class TrendModelTestCase(TestCase):
    """This class defines the test suite for the models."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.name = "Test_trend"
        self.tweet_volume = 0
        self.url = "test/url"
        self.trend = models.Trend(
            name=self.name, tweet_volume=self.tweet_volume,
            url=self.url
        )
        models.Trend.objects.create(
            name='setUp_trend', tweet_volume=self.tweet_volume,
            url=self.url
        )

    def test_model_can_create_a_trend(self):
        """Test the Trend model can create a trend."""
        old_count = models.Trend.objects.count()
        self.trend.save()
        new_count = models.Trend.objects.count()
        print(new_count)
        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_a_trend(self):
        """Test the Trend model can create a trend."""
        new_count = models.Trend.objects.count()
        print(new_count)
        trend = models.Trend.objects.get(name='setUp_trend')
        self.assertEqual(trend.name, 'setUp_trend')

    def test_model_can_get_or_create_a_trend(self):
        """Test the Trend model can create a trend."""
        trend = models.Trend.objects.get_or_create(
            name='setUp_trend', tweet_volume=self.tweet_volume,
            url=self.url
        )
        self.assertEqual(next(iter(trend)).name, 'setUp_trend')

    def test_model_gets_a_trend_if_exists(self):
        """Test the Trend model can create a trend."""
        trend = models.Trend.objects.get_or_create(
            name='setUp_trend', tweet_volume=self.tweet_volume,
            url=self.url
        )
        self.assertEqual(trend[1], False)

    def test_model_creates_a_trend_if_not_exists(self):
        """Test the Trend model can create a trend."""
        trend = models.Trend.objects.get_or_create(
            name="new_name", tweet_volume=self.tweet_volume,
            url=self.url
        )
        self.assertEqual(trend[1], True)


class ViewTrendTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.trend_data = {
            'name': 'api_created',
            'tweet_volume': 1001,
            'url': 'api/created/url'
        }
        self.response = self.client.post(
            reverse('create'),
            self.trend_data,
            format="json")

    def test_api_can_create_a_trend(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
