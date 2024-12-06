from django.contrib import admin
from django.urls import path, include
from .views import LoginWithUsernameAPIView, LogoutAPIView, ResgisterAPIView, VerifyEmailnActivateAPIAccountView

urlpatterns = [
    path('username/login', LoginWithUsernameAPIView.as_view(), name='username_login'),
    path('register', ResgisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='login'),
    path('verify-email-and-activate-account', VerifyEmailnActivateAPIAccountView.as_view(), name='verify_email_and_activate_account'),
]
