from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginWithUsernameAPISerializer, LogoutAPISerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

class LoginWithUsernameAPIView(APIView):
    def post(self, request):
        serializer = LoginWithUsernameAPISerializer(data=request.data)
        if (serializer.is_valid()):
            data = serializer.validated_data
            username = data['username']
            password = data['password']

            user = authenticate(request, username=username, password=password)

            if (user):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "token": token.key,
                    "__c__": created,
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = LogoutAPISerializer(data=request.data)
            if (serializer.is_valid()):
                data = serializer.validated_data
                print(data['logout_all_devices'])
                if (data['logout_all_devices']):
                    token = Token.objects.get(user=request.user)
                    token.delete()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)
