from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from post_saver import views
from post_saver.scripts import scheduler

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='Post')
router.register(r'titles', views.TitleViewSet, basename='Title')
router.register(r'savedposts', views.SavedPostViewSet, basename='SavedPost')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]

if settings.DEBUG:
    scheduler.start()
