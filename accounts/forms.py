from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    telegram_id = forms.IntegerField(label="Telegram ID", required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "telegram_id", "password1", "password2")


class LoginForm(forms.Form):
    telegram_id = forms.IntegerField(label="Telegram ID", required=True)

    def clean(self):
        cleaned_data = super().clean()
        tg_id = cleaned_data.get("telegram_id")

        if tg_id:
            try:
                user = CustomUser.objects.get(telegram_id=tg_id)
                cleaned_data["user"] = user
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким Telegram ID не найден")

        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get("user")
