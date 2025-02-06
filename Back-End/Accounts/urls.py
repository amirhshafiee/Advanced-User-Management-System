from django.urls import path
from . import views

app_name = 'user-page'

urlpatterns = [

    path('register/', views.RegisterView.as_view(), name='register-page'),
    path('register/verify-otp/', views.VerifyRegisterOTPView.as_view(), name='verify-otp-page'),

    path('login/', views.LoginView.as_view(), name='login-page'),
    path('login/refresh/', views.RefreshView.as_view(), name='login-refresh-page'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),


    path('password/forget/', views.ForgetPasswordView.as_view(), name='forget-password-page'),
    path('password/forget/verify/', views.VerifyForgetPasswordOTPView.as_view(), name='verify-forget-password-page'),
    path('password/reset/', views.SetNewPasswordView.as_view(), name='set-password-page'),
    path('profile/password-reset/', views.PasswordResetView.as_view(), name='password-reset-page'),


    path('profile/', views.ProfileView.as_view(), name='profile-page'),
]
