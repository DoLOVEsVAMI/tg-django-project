from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.contrib.auth import login
from django.contrib.auth import get_user_model
import json

User = get_user_model()
# список Telegram ID, которым назначается роль "admin"
ALLOWED_TG_IDS = [425001521, 772350098]  # замени на свои ID
@csrf_exempt
def telegram_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            tg_id = data.get("telegram_id")
            username = data.get("username", f"user_{tg_id}")
            first_name = data.get("first_name", "")

            if not tg_id:
                return JsonResponse({"status": "error", "message": "No telegram_id"})

            user, created = User.objects.get_or_create(telegram_id=tg_id)

            if created:
                user.username = username
                user.first_name = first_name
                user.role = "admin" if int(tg_id) in ALLOWED_TG_IDS else "user"
                user.set_unusable_password()  # пароль не нужен
                user.save()

            # автоматический вход
            login(request, user)

            return JsonResponse({
                "status": "ok",
                "message": "Login successful",
                "role": user.role
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def register_view(request):
    """
    Регистрация пользователя.
    Проверяем Telegram ID и назначаем роль admin или user.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            tg_id = form.cleaned_data.get("telegram_id")
            user.telegram_id = tg_id

            # проверка роли
            if tg_id in ALLOWED_TG_IDS:
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
    """
    Логин по Telegram ID (без пароля).
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """
    Выход пользователя.
    """
    logout(request)
    return redirect("login")
