from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)
    role = models.CharField(max_length=50, default="user")  # роли: user, admin, vip и т.д.

    def __str__(self):
        return self.username
