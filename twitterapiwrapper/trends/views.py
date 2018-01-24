from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


from . import serializers
from . import models


class TrendListCreateView(generics.ListCreateAPIView):
    """
    This class defines the create and get list behavior of trends.
    """
    queryset = models.Trend.objects.all()
    serializer_class = serializers.TrendSerializer


class TrendRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    This class defines retrieve, update, get behavior of trends.
    """
    queryset = models.Trend.objects.all()
    serializer_class = serializers.TrendSerializer


# class TweetListCreateView(generics.ListCreateAPIView):
#     """
#     This class defines the create behavior of our rest api.
#     """
#     queryset = models.Tweet.objects.all()
#     serializer_class = serializers.TweetSerializer
#
#
# class TrendRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """This class defines retrieve, update, get"""
#     queryset = models.Tweet.objects.all()
#     serializer_class = serializers.TweetSerializer


class TweetListCreateView(generics.GenericAPIView):
    """
    This class defines the create behavior of our rest api.
    """
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer

    def get(self, request, trend_id, format=None):
        tweets = self.queryset.filter(trend_id=trend_id)
        serializer = self.serializer_class(tweets, many=True)
        return Response(serializer.data)

    def post(self, request, trend_id, format=None):
        serializer = serializers.TweetSerializer(data=request.data, context={'trend_id': trend_id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)