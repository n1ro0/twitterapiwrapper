from django.db import models


class TrendQuerySet(models.QuerySet):
    def popular(self):
        return self.filter(tweet_volume__gte=10000)
    popular.queryset_only = False


class TweetQuerySet(models.QuerySet):
    def without_hashtags(self):
        return self.all()
    without_hashtags.queryset_only = False


class HashtagQuerySet(models.QuerySet):
    pass
