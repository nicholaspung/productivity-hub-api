from django.contrib import admin
from open_apps.models.vice import Vice, ViceAnalytic, ViceThreshold


class ViceAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'link', 'analytic', 'archived']


class ViceAnalyticAdmin(admin.ModelAdmin):
    fields = ['user', 'frequency', 'date', 'vice', 'threshold', 'last_updated']


class ViceThresholdAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'threshold']


admin.site.register(Vice, ViceAdmin)
admin.site.register(ViceAnalytic, ViceAnalyticAdmin)
admin.site.register(ViceThreshold, ViceThresholdAdmin)
