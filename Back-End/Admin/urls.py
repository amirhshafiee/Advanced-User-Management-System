from django.urls import path
from . import views

app_name = 'admin-page'
urlpatterns = [
    path('users/', views.UsersView.as_view(), name= 'users-page'),
    path('users/<str:email>/', views.UpdateUserView.as_view(), name='update-user-page'),
    path('actions/', views.ActivityLogView.as_view(), name='activity-log--page'),

]