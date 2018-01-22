from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
