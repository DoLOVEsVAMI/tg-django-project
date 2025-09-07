from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from .models import CustomUser
import json

# Telegram ID, которым даём роль администратора
ALLOWED_TG_IDS = [425001521, 772350098]  # замени на свои ID

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.telegram_id = form.cleaned_data.get("telegram_id")

            if user.telegram_id in ALLOWED_TG_IDS:
                user.role = "admin"
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


# ✅ Telegram Mini App Login
@csrf_exempt
def telegram_login(request):
    if request.method == "GET":
        # Открываем страницу мини-приложения
        return render(request, "accounts/telegram_login.html")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tg_id = data.get("telegram_id")
            username = data.get("username", "")
            first_name = data.get("first_name", "")

            if not tg_id:
                return JsonResponse({"status": "error", "message": "No telegram_id provided"})

            # Проверяем, есть ли пользователь
            user, created = CustomUser.objects.get_or_create(
                telegram_id=tg_id,
                defaults={"username": username or f"user_{tg_id}", "first_name": first_name}
            )

            # Назначаем роль
            if int(tg_id) in ALLOWED_TG_IDS:
                user.role = "admin"
            else:
                user.role = "user"

            user.save()
            login(request, user)

            return JsonResponse({"status": "ok", "role": user.role})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})
