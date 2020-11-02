from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from firebase_auth import views
from firebase_auth.scripts import scheduler

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename="User")
router.register(r'profile', views.ProfileViewSet, basename="Profile")
router.register(r'useranalytics', views.UserAnalyticViewSet,
                basename="UserAnalytic")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]

if settings.DEBUG:
    scheduler.start()
