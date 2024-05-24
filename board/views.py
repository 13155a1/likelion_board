from django.shortcuts import render
from .models import Post, Comment, Like
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer, PostCreateSerializer, PostCommentCreateSerializer, LikeSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view

# custom permission
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# post
class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'likes_count']
    ordering = '-created_at'

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
        message = "저장되었습니다"
        return Response({"message": message, "data" : data}, status=status.HTTP_201_CREATED)

class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = response.data
        message = "수정되었습니다."
        return Response({"message": message, "data" : data}, status=status.HTTP_200_OK)

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
        message = "저장되었습니다"
        return Response({"message": message, "data" : data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def user_post_like_true_or_false(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    try: 
        like = Like.objects.get(user=user, post=post)
    except:
        return Response({"like": False}, status=status.HTTP_200_OK)
    
    return Response({"like": True}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    if Like.objects.filter(user=user, post=post).exists():
        return Response({"error": "이미 좋아요가 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

    like = Like(
        user=user,
        post=post
    )
    like.save()

    like_serializer = LikeSerializer(like)

    data = like_serializer.data
    message = "저장되었습니다."

    return Response({"message": message, "data" : data}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    print(user.name)
    print(post.title)

    try: 
        like = Like.objects.get(user=user, post=post)
    except:
        return Response({"error": "좋아요가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    like.delete()

    return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)