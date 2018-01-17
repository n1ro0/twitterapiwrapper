import os


from celery import Celery
# from celery.task.control import inspect


# from apiwrapperapp import tasks


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitterapiwrapper.settings')
app = Celery('twitterapiwrapper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(60.0, save_tweets.s(), name='updates every minute')