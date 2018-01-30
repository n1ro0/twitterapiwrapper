from django.utils import timezone


from rest_framework.test import APITestCase


from ... import models


class HashtagModelAPITestCase(APITestCase):
    def setUp(self):
        self.text = "test_hashtag"
        self.hashtag = models.Hashtag(text=self.text)

    def test_model_can_create_a_hashtag(self):
        initial_count = models.Hashtag.objects.count()
        self.hashtag.save()
        new_count = models.Hashtag.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_model_can_get_a_hashtag(self):
        self.hashtag.save()
        hashtag = models.Hashtag.objects.get(pk=self.hashtag.pk)
        self.assertEqual(self.hashtag, hashtag)
        self.assertEqual(self.hashtag.id, hashtag.id)

    def test_model_can_delete_a_hashtag(self):
        self.hashtag.save()
        initial_count = models.Hashtag.objects.count()
        self.hashtag.delete()
        new_count = models.Hashtag.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_model_can_add_tweets_to_hashtag(self):
        self.hashtag.save()
        new_trend = models.Trend.objects.create(
            name='new_name',
            tweet_volume=22222,
            url='https://newtrend.com/api/trend/ok'
        )
        tweet = models.Tweet.objects.create(
            username='new_username',
            published=timezone.now(),
            text='new_text',
            trend=new_trend
        )
        tweet1 = models.Tweet.objects.create(
            username='new_username1',
            published=timezone.now(),
            text='new_text1',
            trend=new_trend
        )
        models.Tweet.objects.create(
            username='new_username2',
            published=timezone.now(),
            text='new_text2',
            trend=new_trend
        )
        hashtag = models.Hashtag.objects.prefetch_related('tweets').get()
        hashtag.tweets.add(tweet)
        hashtag.tweets.add(tweet1)
        self.assertEqual(models.Tweet.objects.count(), 3)
        self.assertEqual(hashtag.tweets.count(), 2)

