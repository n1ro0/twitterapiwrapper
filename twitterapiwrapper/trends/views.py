from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import (
    detail_route,
    list_route
)

from . import serializers
from . import models


class TweetsModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing trend instances.
    """
    serializer_class = serializers.TweetSerializer
    queryset = models.Tweet.objects.all()

    @detail_route(methods=['get'])
    def hashtags(self, request, pk=None):
        hashtags = models.Tweet.objects.get(pk=pk).hashtags.all()
        serializer = serializers.HashtagSerializer(hashtags, many=True)
        return Response(serializer.data)


class HashtagsModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing trend instances.
    """
    serializer_class = serializers.HashtagSerializer
    queryset = models.Hashtag.objects.all()

    @detail_route(methods=['get'])
    def tweets(self, request, pk=None):
        tweets = models.Hashtag.objects.filter(pk=pk).prefetch_related('tweets').get(pk=pk).tweets
        serializer = serializers.TweetSerializer(tweets, many=True)
        return Response(serializer.data)


class TrendsModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing trend instances.
    """
    serializer_class = serializers.TrendSerializer
    queryset = models.Trend.objects.all()

    @detail_route(methods=['get'])
    def tweets(self, request, pk=None):
        tweets = models.Tweet.objects.filter(trend_id=pk)
        serializer = serializers.TweetSerializer(tweets, many=True)
        return Response(serializer.data)
        # new_data = {
        #     'username': request.data['username'],
        #     'created_at': request.data['created_at'],
        #     'text': request.data['text'],
        #     'trend': pk,
        # }
        # serializer = serializers.TweetSerializer(data=new_data)
        #
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def recent_trends(self, request):
        recent_trends = models.Trend.objects.all().order_by('-created')

        page = self.paginate_queryset(recent_trends)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_trends, many=True)
        return Response(serializer.data)


# class TrendListCreateView(generics.ListCreateAPIView):
#     """
#     This class defines the create and get list behavior of trends.
#     """
#     queryset = models.Trend.objects.all()
#     serializer_class = serializers.TrendSerializer
#
#
# class TrendRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     This class defines retrieve, update, get behavior of trends.
#     """
#     queryset = models.Trend.objects.all()
#     serializer_class = serializers.TrendSerializer
#
#     @detail_route(methods=['get'], url_name='tweets')
#     def tweets(self, request, pk=None):
#         tweets = models.Tweet.objects.filter(trend_id=pk)
#         serializer = serializers.TweetSerializer(tweets, many=True)
#         return Response(serializer.data)


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


# class TweetListCreateView(generics.GenericAPIView):
#     """
#     This class defines the create behavior of our rest api.
#     """
#     queryset = models.Tweet.objects.all()
#     serializer_class = serializers.TweetSerializer
#
#     def get(self, request, trend_id, format=None):
#         tweets = self.queryset.filter(trend_id=trend_id)
#         serializer = self.serializer_class(tweets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, trend_id, format=None):
#         new_data = {
#             'username': request.data['username'],
#             'created_at': request.data['created_at'],
#             'text': request.data['text'],
#             'trend': trend_id,
#         }
#         serializer = serializers.TweetSerializer(data=new_data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TweetListCreateView(generics.ListCreateAPIView):
#     """
#     This class defines the create behavior of our rest api.
#     """
#     queryset = models.Tweet.objects.all()
#     serializer_class = serializers.TweetSerializer
#
#     def get_queryset(self):
#         queryset = models.Tweet.objects.all()
#         return queryset



