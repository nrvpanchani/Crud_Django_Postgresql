from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('<int:id>/', views.comment_thread, name='thread'),
    path('<int:id>/delete/', views.comment_delete, name='delete'),
]