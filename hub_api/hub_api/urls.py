from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG

urlpatterns = [
    path('api/', include('habit_tracker.urls')),
    path('api/', include('firebase_auth.urls')),
    path('api/', include('post_saver.urls')),
]

if DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
