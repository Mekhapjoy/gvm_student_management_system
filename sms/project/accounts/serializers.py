from rest_framework import serializers
from accounts.models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['email','password']