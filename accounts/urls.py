from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, telegram_login_view


urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("telegram-login/", telegram_login_view, name="telegram-login"),
]
