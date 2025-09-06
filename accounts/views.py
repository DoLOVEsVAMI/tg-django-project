from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# список Telegram ID, которым назначается роль "admin"
ADMIN_TG_IDS = [425001521, 772350098]  # замени на свои ID


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
            if tg_id in ADMIN_TG_IDS:
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
@csrf_exempt
def telegram_login_view(request):
    if request.method == "POST":
        tg_id = request.POST.get("telegram_id")
        if tg_id:
            # ищем пользователя по Telegram ID
            try:
                user = CustomUser.objects.get(telegram_id=tg_id)
                login(request, user)
                return JsonResponse({"status": "ok", "message": "Logged in"})
            except CustomUser.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"})
        return JsonResponse({"status": "error", "message": "No telegram_id"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
