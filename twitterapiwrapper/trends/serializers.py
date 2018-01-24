from rest_framework import serializers


from . import models


class TrendSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.Trend
        fields = (
            'id', 'name', 'tweet_volume',
            'url', 'created', 'modified'
        )
        read_only_fields = ('created', 'modified')


class TweetSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.Tweet
        fields = (
            'id', 'username', 'created_at',
            'text', 'trend_id', 'created',
            'modified'
        )
        read_only_fields = ('created', 'modified')