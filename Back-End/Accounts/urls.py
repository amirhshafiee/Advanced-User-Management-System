from django.urls import path
from . import views

app_name = 'user-page'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name= 'register-page'),
    path('register/verify-opt/', views.VerifyOTPView.as_view(), name='verify-opt-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('login/refresh/', views.LoginRefreshView.as_view(), name= 'login-refresh-page'),
    path('profile/', views.ProfileView.as_view(), name='profile-page'),
    path('profile/password-reset/', views.PasswordResetView.as_view(), name='password-reset-page'),

]