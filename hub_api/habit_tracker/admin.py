from django.contrib import admin

from .models import Daily, Habit, Todo


class TodoAdmin(admin.ModelAdmin):
    fields = ['name', 'description',
              'finished', 'priority', 'user']


class HabitAdmin(admin.ModelAdmin):
    fields = ['name', 'description',
              'user', 'archived', 'order']


class DailyAdmin(admin.ModelAdmin):
    fields = ['habit', 'finished', 'user']


admin.site.register(Todo, TodoAdmin)
admin.site.register(Habit, HabitAdmin)
admin.site.register(Daily, DailyAdmin)
