from rest_framework import serializers
from .models import CustomUser
import re


class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only= True)
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = CustomUser.objects.create_user(**validated_data)
        return user


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('passwords must be match ...')
        return attrs


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'register_time']

class PasswordResetSerializers(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, datas):
        if datas['new_password'] != datas['confirm_new_password']:
            raise serializers.ValidationError('passwords must be match ...')

        password = datas['new_password']
        if re.match(r'^\d*$', password) or re.match(r'^\D*$', password):
            raise serializers.ValidationError('The password must include at least one alphabetical character and one numeric digit.')
        if len(password) <= 10:
            raise serializers.ValidationError('Password must be at least 10 characters long.')

        return datas