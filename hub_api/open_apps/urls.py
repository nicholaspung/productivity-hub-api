from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from open_apps.views import post_saver as ps_views
from open_apps.scripts.ap_scheduler_post_saver import scheduler as ps_scheduler
from open_apps.views import habit_tracker as ht_views
from open_apps.views import firebase_auth as fba_views
from open_apps.scripts.ap_scheduler_firebase_auth import scheduler as fba_scheduler

router = DefaultRouter()

router.register(r'posts', ps_views.PostViewSet, basename='Post')
router.register(r'titles', ps_views.TitleViewSet, basename='Title')
router.register(r'savedposts', ps_views.SavedPostViewSet, basename='SavedPost')

router.register(r'habits', ht_views.HabitViewSet, basename='Habit')
router.register(r'todos', ht_views.TodoViewSet, basename='Todo')
router.register(r'dailies', ht_views.DailyViewSet, basename='Daily')

router.register(r'user', fba_views.UserViewSet, basename="User")
router.register(r'profile', fba_views.ProfileViewSet, basename="Profile")
router.register(r'useranalytics', fba_views.UserAnalyticViewSet,
                basename="UserAnalytic")

urlpatterns = [
    path('', include(router.urls))
]

if settings.DEBUG and not settings.FIRST_TIME:
    ps_scheduler.start()
    fba_scheduler.start()
