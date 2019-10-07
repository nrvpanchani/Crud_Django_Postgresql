from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('create/', views.post_create),
    path('detail/<str:slug>/', views.post_detail, name="detail"),
    path('<str:slug>/edit/', views.post_update, name="update"),
    path('<str:slug>/delete/', views.post_delete),
]