from django.urls import path
from . import views

app_name = 'user-page'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name= 'register-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('profile/', views.ProfileView.as_view(), name='profile-page'),

]