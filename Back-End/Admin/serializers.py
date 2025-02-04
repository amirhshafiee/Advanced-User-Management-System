from rest_framework import serializers
from Accounts.models import CustomUser

class UsersSerializers(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ['email', 'phone_number', 'name', 'register_time']
