from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('post-list/', views.PostListView.as_view()),
    path('post-create/', views.PostCreateView.as_view()),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view()),
    path('post-detail/<int:pk>/update/', views.PostUpdateView.as_view()),
    path('post-detail/<int:pk>/delete/', views.PostDestroyView.as_view()),
    path('post-detail/<int:post_id>/comment-list/', views.PostCommentsView.as_view()),
    path('post-detail/<int:post_id>/comment-create/', views.PostCommentCreateView.as_view()),
    path('post-detail/<int:post_id>/like/', views.user_post_like_true_or_false),
    path('post-detail/<int:post_id>/like/create/', views.create_like),
    path('post-detail/<int:post_id>/like/delete/', views.delete_like),
]