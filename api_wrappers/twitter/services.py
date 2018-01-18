from api_wrappers.twitter.client import APIWrapper


from .client import APIWrapper


class DatabaseService:
    def __init__(self, models, consumer_key, consumer_secret):
        self.client = APIWrapper(consumer_key, consumer_secret)
        self.models = models

    def get_trends(self):
        return self.client.get_trends()

    def save_trend(self, trend):
        result = self.models.Trend.objects.get_or_create(
            name=trend['name'],
            tweet_volume=trend['tweet_volume'],
            url=trend['url'])
        saved_trend = next(iter(result))
        for tweet in self.client.search_tweets(trend_name=trend['name']):
            self.save_tweet(tweet, saved_trend.pk)
        return saved_trend

    def save_tweet(self, tweet, trend_id):
        result = self.models.Tweet.objects.get_or_create(
            username=tweet.username,
            created_at=tweet.created_at,
            trend_id=trend_id,
            text=tweet.text)
        saved_tweet = next(iter(result))
        print(len(tweet.hashtags))

        for hashtag in tweet.hashtags:
            saved_hashtag = self.save_hashtag(hashtag)
            saved_tweet.hashtags.add(saved_hashtag)
        return saved_tweet

    def save_hashtag(self, hashtag):
        result = self.models.Hashtag.objects.get_or_create(
            text=hashtag.text
        )
        saved_hashtag = next(iter(result))
        return saved_hashtag
