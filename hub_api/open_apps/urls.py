from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from open_apps.views import post_saver_views as ps_views
from open_apps.views import habit_tracker_views as ht_views
from open_apps.views import firebase_auth_views as fba_views
from open_apps.views import app_views as a_views
from open_apps.scripts.ap_scheduler_post_saver import scheduler as ps_scheduler
from open_apps.scripts.ap_scheduler_firebase_auth import scheduler as fba_scheduler

router = DefaultRouter()

router.register(r'titles', ps_views.TitleViewSet, basename='Title')
router.register(r'savedposts', ps_views.SavedPostViewSet, basename='SavedPost')
router.register(r'habits', ht_views.HabitViewSet, basename='Habit')
router.register(r'todos', ht_views.TodoViewSet, basename='Todo')
router.register(r'dailies', ht_views.DailyViewSet, basename='Daily')
router.register(r'profile', fba_views.ProfileViewSet, basename='Profile')
router.register(r'vicethreshold', fba_views.ViceThresholdViewset,
                basename="ViceThreshold")

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/', fba_views.UserAPIView.as_view(), name="user-delete"),
    path('posts/', ps_views.PostAPIView.as_view(), name="posts-view"),
    path('useranalytics/', fba_views.UserAnalyticAPIView.as_view(),
         name="useranalytics-view"),
    path('apps/', a_views.AppAPIView.as_view(), name="apps")
]

if settings.DEBUG and not settings.FIRST_TIME:
    ps_scheduler.start()
    fba_scheduler.start()
