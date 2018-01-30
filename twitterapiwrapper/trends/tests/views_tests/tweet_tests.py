from django.utils import timezone


from rest_framework.test import APITestCase
from rest_framework import status


from ... import models
from ... import serializers


class TweetAPITestCase(APITestCase):
    def setUp(self):
        self.base_url = '/tweets/'
        self.trend = models.Trend.objects.create(
            name='setUp_name',
            tweet_volume=100,
            url='https://setUp.com/url/ok'
        )
        self.tweet_data = {
            'username': 'setUp_username',
            'published': timezone.now(),
            'text': 'setUp_text',
            'trend': self.trend.id
        }
        models.Tweet.objects.create(
            username='test',
            published=timezone.now(),
            text='test',
            trend_id=self.trend.id
        )
        models.Tweet.objects.create(
            username='test',
            published=timezone.now(),
            text='test',
            trend_id=self.trend.id
        )

    def test_get_list_of_tweets(self):
        count = models.Tweet.objects.count()
        response = self.client.get(self.base_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)

    def test_create_a_tweet(self):
        initial_count = models.Tweet.objects.count()
        response = self.client.post(self.base_url, self.tweet_data)
        new_count = models.Tweet.objects.count()
        tweet = models.Tweet.objects.get(id=response.data['id'])
        self.assertNotEqual(initial_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], tweet.id)

    def test_get_a_tweet(self):
        """
        Ensures that we can get tweet by id.
        :return None:
        """
        tweet = models.Tweet.objects.first()
        url = self.base_url + '{}/'.format(tweet.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], tweet.id)
        self.assertEqual(response.data['trend'], tweet.trend_id)

    def test_modify_a_tweet(self):
        """
        Ensures that we can update tweet by id.
        :return None:
        """
        tweet = models.Tweet.objects.first()
        url = self.base_url + '{}/'.format(tweet.id)
        response = self.client.put(url, self.tweet_data)
        updated_tweet = models.Tweet.objects.get(pk=tweet.pk)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(tweet.id, response.data['id'])
        self.assertNotEqual(tweet.username, updated_tweet.username)
        self.assertEqual(updated_tweet.username, response.data['username'])

    def test_delete_a_tweet(self):
        """
        Ensures that we can delete tweet by id.
        :return None:
        """
        tweet = models.Tweet.objects.first()
        initial_count = models.Tweet.objects.count()
        url = self.base_url + '{}/'.format(tweet.id)
        response = self.client.delete(url, format='json')
        new_count = models.Tweet.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(initial_count, new_count)

    def test_get_hashtags_of_tweet(self):
        tweet = models.Tweet.objects.first()
        hashtag_1 = models.Hashtag.objects.create(text='new_hashtag')
        hashtag_2 = models.Hashtag.objects.create(text='new_hashtag')
        hashtag_3 = models.Hashtag.objects.create(text='new_hashtag')
        models.Hashtag.objects.create(text='new_hashtag')
        tweet.hashtags.set((hashtag_1, hashtag_2, hashtag_3))
        url = self.base_url + '{}/hashtags/'.format(tweet.id)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), tweet.hashtags.count())
