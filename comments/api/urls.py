from django.contrib import admin
from django.urls import path, include
from .views import CommentListAPIView, CommentDetailAPIView, CommentCreateAPIView

app_name = "comments-api"

urlpatterns = [
	path('', CommentListAPIView.as_view(), name='list'),
	path('create/', CommentCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='thread'),
   	#path('<int:id>/delete/', views.comment_delete, name='delete'),
]