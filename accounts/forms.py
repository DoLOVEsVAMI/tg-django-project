from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    telegram_id = forms.CharField(required=True, label="Telegram ID")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "telegram_id", "password1", "password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
