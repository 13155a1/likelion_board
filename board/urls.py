from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('post-list/', views.PostListView.as_view()),
    path('post-create/', views.PostCreateView.as_view()),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view()),
    path('post-detail/<int:post_id>/comment-list/', views.PostCommentsView.as_view()),
    path('post-detail/<int:post_id>/comment-create/', views.PostCommentCreateView.as_view()),
]