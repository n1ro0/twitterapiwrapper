from django.urls import path


from rest_framework.urlpatterns import format_suffix_patterns


from . import views

urlpatterns = {
    path(r'', views.TrendListCreateView.as_view(), name="create"),
    path(r'<int:pk>/', views.TrendRetrieveUpdateDestroyAPIView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
