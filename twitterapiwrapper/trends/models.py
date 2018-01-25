from django.db import models

from twitterapiwrapper.core import models as core_models


# class PollManager(models.Manager):
#     def with_counts(self):
#         from django.db import connection
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT p.id, dense_rank() OVER (
#                                                             PARTITION BY p.id
#                                                             ORDER BY p.created DESC
#                                                           )
#                 FROM trends_hashtag p
#                 WHERE p.id < 100
#                 ORDER BY p.id DESC""")
#             result_list = []
#             for row in cursor.fetchall():
#                 print(row)
#                 # p = self.model(id=row[0], question=row[1], poll_date=row[2])
#                 # p.num_responses = row[3]
#                 # result_list.append(p)
#         return result_list
#
#
# class MyManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super(MyManager, self).get_queryset()
#     def custom_method(self, **kwargs):
#         print(self.model)
#         return self.filter(id__lte=10, **kwargs)
#
#
# class NewManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super(MyManager, self).get_queryset()
#     def custom_method(self, **kwargs):
#         print(self.model)
#         return self.filter(id__lte=10, **kwargs)
class Trend(core_models.TimeStampedModel):
    name = models.CharField(max_length=200)
    tweet_volume = models.IntegerField()
    url = models.URLField(max_length=300)

    def __str__(self):
        return self.name


class Hashtag(core_models.TimeStampedModel):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Tweet(core_models.TimeStampedModel):
    username = models.CharField(max_length=50)
    created_at = models.CharField(max_length=200)
    text = models.TextField()
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, related_name='tweets')

    class Meta:
        base_manager_name = 'objects'

    def __str__(self):
        return self.text
