from django.core.handlers.base import reset_urlconf
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializers, LoginSerializers, ProfileSerializers, PasswordResetSerializers
from .models import CustomUser
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect

class RegisterView(APIView):
    def post(self, request):
        ser_data = RegisterSerializers(data= request.data)
        if ser_data.is_valid():
            user = ser_data.create(ser_data.validated_data)
            refresh_token = RefreshToken.for_user(user)
            return Response(data= {
                'Access Token': str(refresh_token.access_token),
                'Refresh Token': str(refresh_token),
            }, status=status.HTTP_201_CREATED)

        return Response(data= ser_data.errors,
                        status= status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        ser_data = LoginSerializers(data= request.data)
        if ser_data.is_valid():
            username = ser_data.validated_data['username']
            password = ser_data.validated_data['password']

            if '@' in username:
                user = CustomUser.objects.filter(email= username).first()
            else:
                user = CustomUser.objects.filter(phone_number= password).first()
            if not user:
                return Response(data= {
                    'Error': 'Email/Phone_number is not valid ...'
                }, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response(data={
                    'Error': 'Password is not valid ...'
                }, status=status.HTTP_400_BAD_REQUEST)
            refresh_token = RefreshToken.for_user(user)

            user.last_login = datetime.now()
            user.save()

            return Response(data={
                'Access Token': str(refresh_token.access_token),
                'Refresh Token': str(refresh_token),
            }, status=status.HTTP_200_OK)

        return Response(data=ser_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user = CustomUser.objects.filter(email= request.user.email).first()
        ser_data = ProfileSerializers(instance= user)
        return Response(data= ser_data.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = CustomUser.objects.filter(email= request.user.email).first()
        ser_data = ProfileSerializers(instance= user, data= request.data, partial= True)
        if ser_data.is_valid():
            ser_data.save()
            return redirect('user-page:profile-page')
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        ser_data = PasswordResetSerializers(data= request.data)
        if ser_data.is_valid():
            user = CustomUser.objects.filter(email= request.user.email).first()
            if not user.check_password(ser_data.validated_data['password']):
                return Response(data= {
                    'Error': 'Old must password not correct!',
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(ser_data.validated_data['new_password'])
            user.save()
            return redirect('user-page:profile-page')

        return Response(data= ser_data.errors, status=status.HTTP_400_BAD_REQUEST)