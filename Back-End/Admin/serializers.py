from rest_framework import serializers
from Accounts.models import CustomUser
from .models import UserActivityLog

class UsersSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ['email', ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'name', 'is_admin', 'register_time']

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserActivityLog
        fields = ['user', 'action', 'timestamp', ]
