import base64
import json


import requests


from . import models


class APIWrapper:
    def __init__(self, consumer_key, consumer_secret):
        self.base_url = 'https://api.twitter.com/'
        self.token = None
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth()


    @property
    def _base64_key_secret(self):
        key_secret = "{}:{}".format(self.consumer_key, self.consumer_secret).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')
        return b64_encoded_key

    def auth(self):
        auth_url = '{}oauth2/token'.format(self.base_url)
        auth_headers = {
            'Authorization': 'Basic {}'.format(self._base64_key_secret),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        auth_data = {
            'grant_type': 'client_credentials'
        }
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
        self.token = json.loads(auth_resp.content.decode()).get('access_token', None)

    def _check_auth(func):
        def wrapper(self, *args, **kwargs):
            if self.token is None:
                self.auth()
            return func(self, *args, **kwargs)
        return wrapper

    @_check_auth
    def get_trends(self, area_id=1):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        url = '{}1.1/trends/place.json?id={}'.format(self.base_url, area_id)
        resp = requests.get(url, headers=headers)
        data = json.loads(resp.content.decode())
        trends_as_dicts = next(iter(data), {}).get("trends", "No trends")
        trends = []
        for trend_as_dict in trends_as_dicts:
            name = trend_as_dict.get('name', 'Not found.')
            tweet_volume = trend_as_dict.get('tweet_volume', None)
            tweet_volume = 0 if tweet_volume is None else tweet_volume
            url = trend_as_dict.get('url', "Not found.")
            trend = models.Trend(name, tweet_volume, url)
            trends.append(trend)
        return trends

    @_check_auth
    def search_tweets(self, trend_name, count=5):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        search_params = {
            'q': trend_name,
            'result_type': 'recent',
            'count': count
        }

        url = '{}1.1/search/tweets.json'.format(self.base_url)
        resp = requests.get(url, headers=headers, params=search_params)
        tweets_as_dicts = json.loads(resp.content.decode()).get('statuses')
        tweets = []
        for tweet_as_dict in tweets_as_dicts:
            text = tweet_as_dict.get("text", None)
            username = tweet_as_dict.get("user", {}).get("name", None)
            created_at = tweet_as_dict.get("created_at", "")
            hashtags_as_dicts = tweet_as_dict.get("entities", {}).get("hashtags", {})
            hashtags = []
            for hashtag_as_dict in hashtags_as_dicts:
                text = hashtag_as_dict.get('text')
                hashtag = models.Hashtag(text)
                hashtags.append(hashtag)
            tweet = models.Tweet(username, created_at, text, hashtags)
            tweets.append(tweet)
        return tweets

    @_check_auth
    def tweets_from_trends(self, trends_count=10, count=5):
        tweets = []
        for index, trend in enumerate(self.get_trends()):
            if index >= trends_count:
                break
            tweets += self.search_tweets(trend.get('name'), count)
        return tweets


if __name__ == "__main__":
    pass
    # CONSUMER_KEY = 'ofWH8kEM24kJZKgWE2KiWUHmC'
    # CONSUMER_SECRET = 'fwjgMf6WYW6F7v5Gnkbya8k4q00PF5XLbRzctvnfXYRtL5c19g'
    # client = APIWrapper(CONSUMER_KEY, CONSUMER_SECRET)
    # trends = client.get_trends()
    # trend = next(iter(trends), "No trends")
    # for tweet in client.search_tweets(trend.name):
    #     print(tweet.to_dict())
