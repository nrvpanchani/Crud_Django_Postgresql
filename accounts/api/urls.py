from django.contrib import admin
from django.urls import path, include
from .views import UserCreateAPIView, UserLoginAPIView

app_name = "users-api"

urlpatterns = [
	path('registration/', UserCreateAPIView.as_view(), name='registration'),
	path('login/', UserLoginAPIView.as_view(), name='login'),

]