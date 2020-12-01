from open_apps.models.post_saver import Post, SavedPost, Title
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'reddit_id', 'title', 'url']
        read_only_fields = ['reddit_id', 'id', 'title', 'url', 'date']


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'title', 'user']
        read_only_fields = ['user', 'id']


class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ['id', 'title', 'url', 'seen', 'user']
        read_only_fields = ['user', 'id', 'title', 'url']
        ordering = ['id']
