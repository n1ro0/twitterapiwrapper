from django.db import models


from twitterapiwrapper.core import models as core_models
from . import managers


class Trend(core_models.TimeStampedModel):
    name = models.CharField(max_length=200)
    tweet_volume = models.IntegerField()
    url = models.URLField(max_length=300)
    objects = managers.TrendManager()

    def to_dict(self):
        new_dict = {
            'name': self.name,
            'tweet_volume': self.tweet_volume,
            'url': self.url
        }
        return new_dict

    def __str__(self):
        return self.name


class Hashtag(core_models.TimeStampedModel):
    text = models.CharField(max_length=200)
    objects = managers.HashtagManager()

    def to_dict(self):
        return {
            "text": self.text
        }

    def __str__(self):
        return self.text


class Tweet(core_models.TimeStampedModel):
    username = models.CharField(max_length=50)
    created_at = models.CharField(max_length=200)
    text = models.TextField()
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, related_name='tweets')
    objects = managers.TweetManager()

    def to_dict(self):
        hashtags = [hashtag.to_dict() for hashtag in self.hashtags.all()]
        new_dict = {'username': self.username, 'created_at': self.created_at, 'text': self.text,
                    'hashtages': hashtags}
        return new_dict

    def __str__(self):
        return self.text
