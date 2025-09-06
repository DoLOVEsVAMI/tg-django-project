from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from .models import CustomUser

# список Telegram ID, которым даём особую роль
ALLOWED_TG_IDS = [123456789, 987654321]  # тут подставь свои ID

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # проверка Telegram ID
            tg_id = int(form.cleaned_data.get("telegram_id"))
            user.telegram_id = tg_id

            if tg_id in ALLOWED_TG_IDS:
                user.role = "vip"
            else:
                user.role = "user"

            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
