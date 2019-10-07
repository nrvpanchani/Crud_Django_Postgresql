from django.contrib import admin
from django.urls import path, include
from .views import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDeteleAPIView, PostCreateAPIView
app_name = 'posts-api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<str:slug>/', PostDetailAPIView.as_view(), name="detail"),
    path('<str:slug>/edit/', PostUpdateAPIView.as_view(), name="update"),
    path('<str:slug>/delete/', PostDeteleAPIView.as_view(), name='delete'),
]