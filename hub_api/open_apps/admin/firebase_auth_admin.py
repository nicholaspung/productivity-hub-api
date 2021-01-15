from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from open_apps.models.firebase_auth import (Profile, UserAnalytic,
                                            UserAnalyticThreshold)

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'is_anonymous', 'apps']


class UserAnalyticAdmin(admin.ModelAdmin):
    fields = ['user', 'label', 'action', 'frequency', 'date', 'threshold']


class UserAnalyticThresholdAdmin(admin.ModelAdmin):
    fields = ['user', 'label', 'threshold']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserAnalytic, UserAnalyticAdmin)
admin.site.register(UserAnalyticThreshold, UserAnalyticThresholdAdmin)
