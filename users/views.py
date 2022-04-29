from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import *


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user


class PasswordEditView(PasswordChangeView):
    form_class = PasswordEditForm
    template_name = 'registration/password-change.html'
    success_url = reverse_lazy('dashboard')

# Create your views here.
