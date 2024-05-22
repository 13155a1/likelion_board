from django.shortcuts import render
from .models import Post
from .serializers import PostListSerializer
from rest_framework.generics import ListAPIView

# Post

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

