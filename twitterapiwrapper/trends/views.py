from django.http import Http404


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


from . import serializers
from . import models


class TrendListCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = models.Trend.objects.all()
    serializer_class = serializers.TrendSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new trend."""
        serializer.save()


class TrendDetail(generics.GenericAPIView):
    """
    Retrieve, update or delete a trend instance.
    """
    serializer_class = serializers.TrendSerializer
    def get_object(self, pk):
        try:
            return models.Trend.objects.get(pk=pk)
        except models.Trend.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        trend = self.get_object(pk)
        serializer = serializers.TrendSerializer(trend)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        trend = self.get_object(pk)
        serializer = serializers.TrendSerializer(trend, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        trend = self.get_object(pk)
        trend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)