from django.contrib import admin

from .models import Post, Title, SavedPost


class PostAdmin(admin.ModelAdmin):
    fields = ['reddit_id', 'title',
              'url']


class TitleAdmin(admin.ModelAdmin):
    fields = ['title',
              'user']


class SavedPostAdmin(admin.ModelAdmin):
    fields = ['title', 'url', 'seen', 'user']


admin.site.register(Post, PostAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(SavedPost, SavedPostAdmin)
