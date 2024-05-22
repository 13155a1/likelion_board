from django.shortcuts import render
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Post

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

