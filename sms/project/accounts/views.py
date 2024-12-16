from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from rest_framework.permissions import IsAdminUser,BasePermission
# Create your views here.

class LoginView(generics.GenericAPIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username = email, password = password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                response = {
                    'refresh':str(refresh),
                    'access':str(access),
                    'is_superuser':user.is_superuser
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                return Response("Invalid email or password",status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class HasPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        return False
            