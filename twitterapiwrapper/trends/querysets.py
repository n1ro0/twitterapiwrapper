from django.db import models


class TrendQuerySet(models.QuerySet):
    def popular(self):
        return self.filter(tweet_volume__gte=10000)
    popular.queryset_only = False


class TweetQuerySet(models.QuerySet):
    def without_hashtags(self):
        return self.annotate(hashtags_count=models.Count('hashtags')).filter(hashtags_count=0)
    without_hashtags.queryset_only = False


class HashtagQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate(tweets_count=models.Count('tweets')).filter(tweets_count__gte=40)
    popular.queryset_only = False
