
from django.contrib import admin
from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordEditView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile-edit/', UserEditView.as_view(), name='profile-edit'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/password-change.html')),
    path('password/', PasswordEditView.as_view()),
 ]
