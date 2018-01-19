from django.contrib import admin


from . import models


# models registration for admin site.
admin.site.register((models.Trend, models.Tweet, models.Hashtag))

