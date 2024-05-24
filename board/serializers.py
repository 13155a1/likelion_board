from rest_framework import serializers
from .models import Post, Comment, Like

# post
class PostListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)
    comments_count = serializers.IntegerField(source='comment.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'user', 'likes_count', 'comments_count']

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'likes_count']

class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

# comment
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user']

class PostCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

# like
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
