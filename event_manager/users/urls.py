from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users-list'),
    path('admin/reset/', views.adminResetPassword, name='users-admin_reset'),
    path('admin/reset/password', views.adminResetPasswordEnter, name='users-admin_reset_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
