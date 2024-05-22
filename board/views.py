from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer, PostCreateSerializer, PostCommentCreateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status

# custom permission
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# post
class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
        data['message'] = "저장되었습니다"
        return Response(data, status=status.HTTP_201_CREATED)

class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = response.data
        data['message'] = "수정되었습니다."
        return Response(data, status=status.HTTP_200_OK)

class PostDestroyView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# comment
class PostCommentsView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        comment_count = queryset.count()
        return Response({
            'comments': serializer.data,
            'total_comments': comment_count
        }, status=status.HTTP_200_OK)

class PostCommentCreateView(CreateAPIView):
    serializer_class = PostCommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(user=self.request.user, post_id=post_id)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
        data['message'] = "저장되었습니다"
        return Response(data, status=status.HTTP_201_CREATED)

