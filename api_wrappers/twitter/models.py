class Hashtag:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.text

    def to_dict(self):
        return {"text": self.text}


class Tweet:
    def __init__(self, username, created_at, text, hashtags):
        self.username = username
        self.created_at = created_at
        self.text = text
        self.hashtags = hashtags

    def __str__(self):
        return self.text

    def to_dict(self):
        hashtags = [hashtag.to_dict() for hashtag in self.hashtags]
        new_dict = {'username': self.username, 'created_at': self.created_at, 'text': self.text,
                    'hashtages': hashtags}
        return new_dict


class Trend:
    def __init__(self, name, tweet_volume, url):
        self.name = name
        self.tweet_volume = tweet_volume
        self.url = url

    def __str__(self):
        return self.name

    def to_dict(self):
        new_dict = {'name': self.name, 'tweet_volume': self.tweet_volume, 'url': self.url}
        return new_dict
