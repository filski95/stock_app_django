from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/customuser_form.html"
    success_url = reverse_lazy("login")
    success_message = "Your profile was created successfully"
