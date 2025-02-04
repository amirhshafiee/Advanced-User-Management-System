from rest_framework import serializers
from .models import CustomUser

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