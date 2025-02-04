from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializers

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
