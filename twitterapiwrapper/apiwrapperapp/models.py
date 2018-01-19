from django.db import models


class Trend(models.Model):
    name = models.CharField(max_length=200)
    tweet_volume = models.IntegerField()
    url = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Hashtag(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Tweet(models.Model):
    username = models.CharField(max_length=50)
    created_at = models.CharField(max_length=200)
    text = models.TextField()
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, related_name='tweets')

    def __str__(self):
        return self.text
