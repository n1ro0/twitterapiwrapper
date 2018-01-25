from django.urls import path


from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


from . import views


router = DefaultRouter()
router.register(r'trends', views.TrendsModelViewSet, base_name='trend')
router.register(r'tweets', views.TweetsModelViewSet, base_name='tweet')
router.register(r'hashtags', views.HashtagsModelViewSet, base_name='hashtag')
urlpatterns = router.get_urls()


# urlpatterns = {
#     path(r'', views.TrendListCreateView.as_view(), name="create"),
#     # path(r'<int:trend_id>/tweets', views.TweetListCreateView.as_view()),
#     path(r'<int:pk>/', views.TrendRetrieveUpdateDestroyAPIView.as_view()),
#
# }

# urlpatterns = format_suffix_patterns(urlpatterns)
