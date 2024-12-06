from rest_framework import serializers

class LoginWithUsernameAPISerializer(serializers.Serializer):
    username = serializers.CharField(required=True)  # Use CharField for username
    password = serializers.CharField(required=True, write_only=True)  # Hide password in responses

class LogoutAPISerializer(serializers.Serializer):
    logout_all_devices = serializers.BooleanField(default=False, required=False)