from django.conf import settings

from celery import shared_task


from . import models


from api_wrappers.twitter.services import DatabaseService


database_service = DatabaseService(models, settings.CONSUMER_KEY, settings.CONSUMER_SECRET)


@shared_task
def save_trend(trend):
    try:
        database_service.save_trend(trend)
    except:
        print("Save trend error")


@shared_task
def save_trends():
    trends = database_service.get_trends()
    for trend in trends:
        save_trend.delay(trend.to_dict())
