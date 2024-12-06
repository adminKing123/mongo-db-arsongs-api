from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

class LoginWithUsernameAPISerializer(serializers.Serializer):
    username = serializers.CharField(required=True)  # Use CharField for username
    password = serializers.CharField(required=True, write_only=True)  # Hide password in responses

class RegisterAPISerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

class LogoutAPISerializer(serializers.Serializer):
    logout_all_devices = serializers.BooleanField(default=False, required=False)