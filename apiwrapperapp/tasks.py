from django.conf import settings

from celery import shared_task

from api_wrappers.twitter.client import APIWrapper
from . import models


# from twitterapiwrapper import settings


client = APIWrapper(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)


class SaveHelper:
    @classmethod
    def save_trend(cls, trend):
        result = models.Trend.objects.get_or_create(
            name=trend['name'],
            tweet_volume=trend['tweet_volume'],
            url=trend['url'])
        saved_trend = next(iter(result))
        for tweet in client.search_tweets(trend_name=trend['name']):
            cls.save_tweet(tweet, saved_trend.pk)
        return saved_trend

    @classmethod
    def save_tweet(cls, tweet, trend_id):
        result = models.Tweet.objects.get_or_create(
            username=tweet.username,
            created_at=tweet.created_at,
            trend_id=trend_id,
            text=tweet.text)
        saved_tweet = next(iter(result))
        for hashtag in tweet.hashtags:
            saved_hashtag = cls.save_hashtag(hashtag)
        saved_tweet.hashtags.add(saved_hashtag)
        return saved_tweet

    @classmethod
    def save_hashtag(cls, hashtag):
        result = models.Hashtag.objects.get_or_create(
            text=hashtag.text
        )
        saved_hashtag = next(iter(result))
        return saved_hashtag


@shared_task
def save_trend(trend):
    try:
        SaveHelper.save_trend(trend)
    except:
        print("Save trend error")


@shared_task
def save_trends():
    trends = client.get_trends()
    for trend in trends:
        save_trend.delay(trend.to_dict())
