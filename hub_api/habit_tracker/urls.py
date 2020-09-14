from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habit_tracker import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'habits', views.HabitViewSet, basename='Habit')
router.register(r'todos', views.TodoViewSet, basename='Todo')
router.register(r'dailies', views.DailyViewSet, basename='Daily')
router.register(r'users', views.UserViewSet, basename="User")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]
