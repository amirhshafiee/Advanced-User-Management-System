from rest_framework import serializers
from Accounts.models import CustomUser

class UsersSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ['email', ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'name', 'is_admin', 'register_time']

