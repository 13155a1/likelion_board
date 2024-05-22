from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('posts/<int:post_id>/comments/', views.PostCommentsView.as_view(), name='post-comments'),
]