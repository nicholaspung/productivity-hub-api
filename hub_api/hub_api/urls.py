from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habit_tracker.urls')),
    path('api/', include('firebase_auth.urls')),
    path('api/', include('post_saver.urls')),
]
