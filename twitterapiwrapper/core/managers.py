from django.db import models


from . import querysets


class BaseManager(models.Manager):
    pass


TimeStampedManager = BaseManager.from_queryset(querysets.TimeStampedQuerySet)
