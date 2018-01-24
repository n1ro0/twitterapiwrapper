from django.db import models
from django.utils import timezone


class CustomManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        return super(CustomManager, self).get_queryset().filter(id__eq=10)

    def custom_method(self, **kwargs):
        print(self.model)
        return self.filter(id__lte=10, **kwargs)


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


