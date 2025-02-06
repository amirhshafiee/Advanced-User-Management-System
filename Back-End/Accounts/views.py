from django.conf import settings
from django.core.handlers.base import reset_urlconf
from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializers, LoginSerializers, ProfileSerializers, PasswordResetSerializers
from .models import CustomUser, EmailOTP
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from Admin.models import UserActivityLog
import random
from django.core.mail import send_mail

class SendOTPAgainView(APIView):
    def post(self, request):
        email = request.data.get('eamil')
        otp = random.randint(100000, 999999)
        EmailOTP.objects.filter(email=email).first().delete()
        EmailOTP.objects.create(email=email, otp=otp)

        send_mail(
            'Email Verify',
            f'Your verification code: {otp}',
            settings.EMAIL_HOST_USER,
            [email, ],
            fail_silently=False,
        )

        return Response(data={
            'Message': 'Verification code sent to email.',
        }, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        #del request.data['otp']

        ser_data = RegisterSerializers(data= request.data)
        if ser_data.is_valid():
            email = EmailOTP.objects.filter(email= ser_data.validated_data['email']).first()

            if not email.is_valid():
                return Response(data= {
                    'Message': 'The verification code has expired!',
                }, status= status.HTTP_400_BAD_REQUEST)

            if email.otp != otp:
                return Response(data= {
                    'Message': 'The verification code is wrong!',
                }, status= status.HTTP_400_BAD_REQUEST)

            user = ser_data.create(ser_data.validated_data)
            refresh_token = RefreshToken.for_user(user)
            UserActivityLog.objects.create(user=user, action='Register')

            email.delete()
            return Response(data={
                'Access Token': str(refresh_token.access_token),
                'Refresh Token': str(refresh_token),
            }, status=status.HTTP_201_CREATED)

        return Response(data=ser_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        ser_data = RegisterSerializers(data= request.data)
        if ser_data.is_valid():
            if EmailOTP.objects.filter(email= ser_data.validated_data['email']).first() != None and EmailOTP.objects.filter(email=ser_data.validated_data['email']).first().is_valid():
                return Response(data= {
                    'Message': 'Email already send it please wait !'
                }, status=status.HTTP_400_BAD_REQUEST)

            otp = random.randint(100000, 999999)
            EmailOTP.objects.create(email=ser_data.validated_data['email'], otp=otp)

            send_mail(
                'Email Verify',
                f'Your verification code: {otp}',
                settings.EMAIL_HOST_USER,
                [ser_data.validated_data['email'], ],
                fail_silently=False,
            )

            return Response(data= {
                'Message': 'Verification code sent to email.',
            }, status= status.HTTP_200_OK)

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

            UserActivityLog.objects.create(user= user, action= 'Login')

            refresh_token = RefreshToken.for_user(user)

            user.last_login = datetime.now()
            user.save()

            return Response(data={
                'Access Token': str(refresh_token.access_token),
                'Refresh Token': str(refresh_token),
            }, status=status.HTTP_200_OK)

        return Response(data=ser_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class LoginRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"Error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                "Access Token": str(refresh.access_token),
                "Refresh Token": str(refresh),

            })
        except Exception:
            return Response({"Error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user = request.user
        ser_data = ProfileSerializers(instance= user)
        return Response(data= ser_data.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        ser_data = ProfileSerializers(instance= user, data= request.data, partial= True)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        ser_data = PasswordResetSerializers(data= request.data)
        if ser_data.is_valid():
            user = CustomUser.objects.filter(email= request.user.email).first()
            if not user.check_password(ser_data.validated_data['password']):
                return Response(data={
                    'Error': 'Incorrect credentials',
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(ser_data.validated_data['new_password'])

            user.save()

            refresh_token = request.data.get('refresh')
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    refresh.blacklist()
                except Exception:
                    return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


        return Response(data= ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        delete = request.data.get('delete')
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({"Error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not delete:
            return Response(data= {
                'Error': 'please set delete value ... '
            }, status= status.HTTP_400_BAD_REQUEST)

        if delete == 'True':
            user = CustomUser.objects.filter(email= request.user.email).first()
            UserActivityLog.objects.create(user= user, action= 'Logout')
            try:
                token = RefreshToken(refresh)
                token.blacklist()
                return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
            except Exception:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                'Error': 'Logout FAILED !!!! '
            }, status=status.HTTP_400_BAD_REQUEST)
