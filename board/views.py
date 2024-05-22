from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Post

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


# comment

class PostCommentsView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)