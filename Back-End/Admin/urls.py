from django.urls import path
from . import views

app_name = 'admin-page'
urlpatterns = [
    path('users/', views.UsersView.as_view(), name= 'users-page'),
]