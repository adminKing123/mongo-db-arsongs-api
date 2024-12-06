from django.contrib import admin
from django.urls import path, include
from .views import LoginWithUsernameAPIView, LogoutAPIView, ResgisterAPIView

urlpatterns = [
    path('username/login', LoginWithUsernameAPIView.as_view(), name='username_login'),
    path('register', ResgisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='login'),
]
