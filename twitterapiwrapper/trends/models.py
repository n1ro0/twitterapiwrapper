from django.db import models

from twitterapiwrapper.core import models as core_models


class Trend(core_models.TimeStampedModel):
    name = models.CharField(max_length=200)
    tweet_volume = models.IntegerField()
    url = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Hashtag(core_models.TimeStampedModel):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Tweet(core_models.TimeStampedModel):
    username = models.CharField(max_length=50)
    created_at = models.CharField(max_length=200)
    text = models.TextField()
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, related_name='tweets')

    def __str__(self):
        return self.text
