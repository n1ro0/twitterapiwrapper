from django.test import TestCase


from ... import models


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
        models.Trend.objects.create(
            name='setUp_trend', tweet_volume=self.tweet_volume,
            url=self.url
        )

    def test_model_can_create_a_trend(self):
        """Test the Trend model can create a trend."""
        old_count = models.Trend.objects.count()
        self.trend.save()
        new_count = models.Trend.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_a_trend(self):
        """Test the Trend model can create a trend."""
        trend = models.Trend.objects.get(name='setUp_trend')
        self.assertEqual(trend.name, 'setUp_trend')

    def test_model_can_modify_a_trend(self):
        """Test the Trend model can create a trend."""
        initial_model = models.Trend.objects.get()
        new_name, new_tweet_volume, new_url = "new_name", 99999, "https://new.com/api/url/okok"
        initial_model.name, initial_model.tweet_volume, initial_model.url = \
            new_name, new_tweet_volume, new_url
        initial_model.save()
        modified_model = models.Trend.objects.get()
        self.assertEqual(initial_model.name, new_name)
        self.assertEqual(initial_model.tweet_volume, new_tweet_volume)
        self.assertEqual(initial_model.url, new_url)
        self.assertEqual(modified_model.name, new_name)
        self.assertEqual(modified_model.tweet_volume, new_tweet_volume)
        self.assertEqual(modified_model.url, new_url)

    def test_model_can_get_or_create_a_trend(self):
        """Test the Trend model can create a trend."""
        trend = models.Trend.objects.get_or_create(
            name='setUp_trend', tweet_volume=self.tweet_volume,
            url=self.url
        )
        self.assertEqual(next(iter(trend)).name, 'setUp_trend')

    def test_model_gets_a_trend_if_exists(self):
        """Test the Trend model can create a trend."""
        trend, created = models.Trend.objects.get_or_create(
            name='setUp_trend', tweet_volume=self.tweet_volume,
            url=self.url
        )
        self.assertEqual(created, False)

    def test_model_creates_a_trend_if_does_not_exist(self):
        """Test the Trend model can create a trend."""
        trend, created = models.Trend.objects.get_or_create(
            name="new_name", tweet_volume=self.tweet_volume,
            url=self.url
        )
        self.assertEqual(created, True)

    def test_model_can_delete_a_trend(self):
        """
        Test the Trend instance can be deleted.
        :return: None
        """
        self.trend.save()
        count = models.Trend.objects.count()
        self.trend.delete()
        new_count = models.Trend.objects.count()
        self.assertEqual(count, new_count + 1)
