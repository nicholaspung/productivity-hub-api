from django.contrib import admin
from open_apps.models.app import App


class AppAdmin(admin.ModelAdmin):
    fields = ['title']


admin.site.register(App, AppAdmin)
