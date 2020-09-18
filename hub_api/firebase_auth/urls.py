from django.urls import include, path
from rest_framework.routers import DefaultRouter

from firebase_auth import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.UserViewSet, basename="User")
router.register(r'profile', views.ProfileViewSet, basename="Profile")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]
