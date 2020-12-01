from django.contrib import admin

from open_apps.models.post_saver import Post, SavedPost, Title


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
