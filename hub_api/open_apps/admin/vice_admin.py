from django.contrib import admin
from open_apps.models.vice import Vice, ViceAnalytic


class ViceAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'link', 'analytic', 'archived']


class ViceAnalyticAdmin(admin.ModelAdmin):
    fields = ['user', 'frequency', 'date',
              'vice', 'last_updated', 'time_between']


admin.site.register(Vice, ViceAdmin)
admin.site.register(ViceAnalytic, ViceAnalyticAdmin)
