from django.contrib import admin
from django.urls import path, include
from .views import LoginWithUsernameAPIView, LogoutAPIView

urlpatterns = [
    path('username/login', LoginWithUsernameAPIView.as_view(), name='username_login'),
    path('logout', LogoutAPIView.as_view(), name='login'),
]
