from rest_framework import generics


from . import serializers
from . import models


class TrendCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = models.Trend.objects.all()
    serializer_class = serializers.TrendSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
