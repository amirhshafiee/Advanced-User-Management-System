from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from Accounts.models import CustomUser
from .permissions import AdminPermission
from .serializers import UsersSerializers

class UsersView(APIView):
    permission_classes = [AdminPermission, ]

    def get(self, request):
        usrs = CustomUser.objects.all()
        ser_data = UsersSerializers(instance= usrs, many= True)
        return Response(data= ser_data.data, status=status.HTTP_200_OK)

