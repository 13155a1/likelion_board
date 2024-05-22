from rest_framework import serializers
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'user', 'likes_count']

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'likes_count']