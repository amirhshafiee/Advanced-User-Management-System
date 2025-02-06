from rest_framework import serializers
from .models import CustomUser
import re

def validate_password_strength(password):
    if re.match(r'^\d*$', password) or re.match(r'^\D*$', password):
        raise serializers.ValidationError('The password must include at least one letter and one number.')
    if len(password) < 10:
        raise serializers.ValidationError('Password must be at least 10 characters long.')




class RegisterSerializer(serializers.ModelSerializer):
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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'register_time']
        extra_kwargs = {
            'email': {'read_only': True},
            'register_time': {'read_only': True},
        }

class PasswordResetSerializers(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, datas):
        if datas['new_password'] != datas['confirm_new_password']:
            raise serializers.ValidationError('Incorrect credentials')

        validate_password_strength(datas['new_password'])
        return datas

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate(self, datas):
        if not CustomUser.objects.filter(email=datas['email']).exists():
            raise serializers.ValidationError('Email is not correct.')

        return datas

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, datas):
        if datas['password'] != datas['confirm_password']:
            raise serializers.ValidationError('Incorrect credentials')
        validate_password_strength(datas['password'])
        return datas
