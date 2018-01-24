from django.urls import path


from rest_framework.urlpatterns import format_suffix_patterns


from . import views

urlpatterns = {
    path(r'^trend/$', views.TrendCreateView.as_view(), name="create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
