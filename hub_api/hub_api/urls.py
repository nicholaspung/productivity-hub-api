from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('habit_tracker.urls')),
    path('api/', include('firebase_auth.urls')),
    path('api/', include('post_saver.urls')),
    path('openapi/', get_schema_view(
        title="Productivity Hub",
        description="API for Productivity Hub. Autogenerated with DjangoRestFramework",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui')
]

if DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
