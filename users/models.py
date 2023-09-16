from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="email", help_text="Введите email"
    )
    username = models.CharField(
        max_length=150, verbose_name="логин", help_text="Введите логин"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
