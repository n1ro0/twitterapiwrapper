from django.test import TestCase
from django.utils import timezone


from ... import models


class TweetModelTestCase(TestCase):
    def setUp(self):
        self.username = "test_username"
        self.published = timezone.now()
        self.text = 'test_text'
        self.trend, self.is_created = models.Trend.objects.get_or_create(
            name='trend_name',
            tweet_volume=1111,
            url='https://trend.com/api/trend/ok'
        )
        self.tweet = models.Tweet(
            username=self.username,
            published=self.published,
            text=self.text,
            trend=self.trend
        )

    def test_model_can_create_a_tweet(self):
        initial_count = models.Tweet.objects.count()
        self.tweet.save()
        new_count = models.Tweet.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_model_can_get_a_tweet(self):
        self.tweet.save()
        tweet = models.Tweet.objects.get()
        self.assertEqual(self.tweet.id, tweet.id)

    def test_model_gets_a_tweet_if_exists(self):
        self.tweet.save()
        tweet, is_created = models.Tweet.objects.get_or_create(
            username=self.username,
            published=self.published,
            text=self.text,
            trend=self.trend
        )
        self.assertEqual(self.tweet.id, tweet.id)
        self.assertEqual(is_created, False)

    def test_model_creates_a_tweet_if_does_not_exist(self):
        self.tweet.save()
        new_trend, trend_is_created = models.Trend.objects.get_or_create(
            name='new_name',
            tweet_volume=22222,
            url='https://newtrend.com/api/trend/ok'
        )
        tweet, tweet_is_created = models.Tweet.objects.get_or_create(
            username='new_username',
            published=self.published,
            text='new_text',
            trend=new_trend
        )
        self.assertNotEqual(self.tweet.id, tweet.id)
        self.assertEqual(tweet_is_created, True)

    def test_model_can_modify_a_tweet(self):
        self.tweet.save()
        tweet = models.Tweet.objects.get()
        new_trend, is_created = models.Trend.objects.get_or_create(
            name='new_name',
            tweet_volume=22222,
            url='https://newtrend.com/api/trend/ok'
        )
        new_username, new_published, new_text = \
            'new_username', timezone.now(), 'new_text'
        tweet.username, tweet.published, tweet.text, tweet.trend = \
            new_username, new_published, new_text, new_trend
        tweet.save()
        new_tweet = models.Tweet.objects.get()
        self.assertEqual(new_tweet.username, new_username)
        self.assertEqual(new_tweet.published, new_published)
        self.assertEqual(new_tweet.text, new_text)
        self.assertEqual(new_tweet.trend_id, new_trend.id)

    def test_model_can_add_hashtags_to_tweet(self):
        self.tweet.save()
        hashtag1 = models.Hashtag(text='new_hashtag1')
        hashtag1.save()
        self.tweet.hashtags.add(hashtag1)
        hashtag2 = models.Hashtag(text='new_hashtag2')
        hashtag2.save()
        self.tweet.hashtags.add(hashtag2)
        self.assertEqual(self.tweet.hashtags.count(), 2)
        self.assertEqual(models.Hashtag.objects.count(), 2)

