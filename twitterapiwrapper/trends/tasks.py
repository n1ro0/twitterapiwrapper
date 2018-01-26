from django.conf import settings


from celery import shared_task


from . import models
from .wrapper import APIWrapper


client = APIWrapper(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)


def save_tweet_with_hashtags(tweet_with_hashtags):
    tweet_with_hashtags[0].save()
    for hashtag in tweet_with_hashtags[1]:
        hashtag.save()
    tweet_with_hashtags[0].hashtags.set(tweet_with_hashtags[1])


@shared_task
def save_trend(trend):
    result = models.Trend.objects.get_or_create(
        **trend
    )
    saved_trend = next(iter(result))
    for tweet_with_hashtags in client.search_tweets(trend_name=saved_trend.name):
        tweet_with_hashtags[0].trend_id = saved_trend.pk
        save_tweet_with_hashtags(tweet_with_hashtags)


@shared_task
def save_trends():
    trends = client.get_trends()
    for trend in trends:
        save_trend.delay(trend.to_dict())
