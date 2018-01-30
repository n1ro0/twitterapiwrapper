from django.utils import timezone


from rest_framework.test import APITestCase
from rest_framework import status


from ... import models
from ... import serializers


class TrendAPITestCase(APITestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.trend_data = {
            'name': 'api_created',
            'tweet_volume': 102,
            'url': 'https://domain.com/api/created/ok'
        }

    def test_get_list_of_trends(self):
        """
        Ensure we can get list of trends
        :return: None
        """
        models.Trend.objects.create(
            name='new_name',
            tweet_volume=22222,
            url='https://newtrend.com/api/trend/ok'
        )
        models.Trend.objects.create(
            name='new_name',
            tweet_volume=22222,
            url='https://newtrend.com/api/trend/ok'
        )
        url = '/trends/'
        trends = models.Trend.objects.all()
        trend_serializer = serializers.TrendSerializer(trends, many=True)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(trend_serializer.data))

    def test_create_trend(self):
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

    def test_get_trend(self):
        """
        Ensures that we can update existed trend
        :return: None
        """
        trend = models.Trend.objects.create(
            name='new_trend',
            tweet_volume=11111,
            url='https://my.com/api/ok'
        )
        url = '/trends/{}/'.format(trend.id)
        response = self.client.get(url, format='json')
        trend_serializer = serializers.TrendSerializer(trend)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], trend_serializer.data['id'])
        self.assertEqual(response.data['name'], trend_serializer.data['name'])
        self.assertEqual(response.data['tweet_volume'], trend_serializer.data['tweet_volume'])
        self.assertEqual(response.data['url'], trend_serializer.data['url'])
        self.assertEqual(response.data['created'], trend_serializer.data['created'])
        self.assertEqual(response.data['modified'], trend_serializer.data['modified'])

    def test_modify_trend(self):
        """
        Ensures that we can update existed trend
        :return: None
        """
        trend = models.Trend.objects.create(
            name='new_trend',
            tweet_volume=11111,
            url='https://my.com/api/ok'
        )
        trend_data = dict(self.trend_data)
        trend_data['id'] = trend.id
        url = '/trends/{}/'.format(trend.id)
        response = self.client.put(url, trend_data, format='json')
        instance = models.Trend.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(instance.name, 'api_created')
        self.assertEqual(instance.tweet_volume, 102)
        self.assertEqual(instance.url, 'https://domain.com/api/created/ok')

    def test_get_trend_tweets(self):
        """
        Ensures that we can update existed trend
        :return: None
        """
        trend = models.Trend.objects.create(
            name='new_trend',
            tweet_volume=11111,
            url='https://my.com/api/ok'
        )
        models.Tweet.objects.create(
            username='new_username',
            published=timezone.now(),
            text='new_text',
            trend=trend
        )
        models.Tweet.objects.create(
            username='new_username1',
            published=timezone.now(),
            text='new_text',
            trend=trend
        )
        models.Tweet.objects.create(
            username='new_username2',
            published=timezone.now(),
            text='new_text',
            trend=trend
        )
        url = '/trends/{}/tweets/'.format(trend.id)
        response = self.client.get(url, format='json')
        count = models.Trend.objects.get().tweet_set.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 3)
        self.assertEqual(len(response.data), 3)

    def test_create_trend_tweet(self):
        """
        Ensures that we can update existed trend
        :return: None
        """
        trend = models.Trend.objects.create(
            name='new_trend',
            tweet_volume=11111,
            url='https://my.com/api/ok'
        )
        models.Tweet.objects.create(
            username='new_username',
            published=timezone.now(),
            text='new_text',
            trend=trend
        )
        models.Tweet.objects.create(
            username='new_username1',
            published=timezone.now(),
            text='new_text',
            trend=trend
        )
        models.Tweet.objects.create(
            username='new_username2',
            published=timezone.now(),
            text='new_text',
            trend=trend
        )
        tweet_data = {
            'username': 'new_username2',
            'published': timezone.now(),
            'text': 'new_text',
        }
        url = '/trends/{}/tweets/'.format(trend.id)
        response = self.client.post(url, tweet_data, format='json')
        count = models.Trend.objects.get().tweet_set.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count, 4)

