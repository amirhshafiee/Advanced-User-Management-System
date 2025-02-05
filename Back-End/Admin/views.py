from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from Accounts.models import CustomUser
from .permissions import AdminPermission
from .serializers import UsersSerializer, UserSerializer

class UsersView(APIView):
    permission_classes = [AdminPermission, ]

    def get(self, request):
        usrs = CustomUser.objects.exclude(email= request.user.email)
        ser_data = UsersSerializer(instance= usrs, many= True)
        return Response(data= ser_data.data, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    permission_classes = [AdminPermission, ]

    def get(self, request, email):
        user = CustomUser.objects.filter(email= email).first()
        ser_data = UserSerializer(instance=user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def patch(self, request, email):
        user = CustomUser.objects.filter(email= email).first()
        ser_dat = UserSerializer(instance=user, data= request.data, partial=True)
        if ser_dat.is_valid():
            ser_dat.save()
            return redirect('admin-page:update-user-page', email= email)
        return Response(data= ser_dat.errors, status=status.HTTP_400_BAD_REQUEST)
