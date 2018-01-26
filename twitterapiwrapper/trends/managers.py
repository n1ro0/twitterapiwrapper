from django.db import models
from . import querysets


class BaseManager(models.Manager):
    pass


TrendManager = BaseManager.from_queryset(querysets.TrendQuerySet)
TweetManager = BaseManager.from_queryset(querysets.TweetQuerySet)
HashtagManager = BaseManager.from_queryset(querysets.HashtagQuerySet)

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
