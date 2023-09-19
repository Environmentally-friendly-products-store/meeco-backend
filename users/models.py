from django.contrib.auth.models import AbstractUser
from django.db import models

from products.models import Product

from .managers import MyUserManager


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="email", help_text="Введите email"
    )
    username = models.CharField(
        max_length=150, verbose_name="логин", help_text="Введите логин"
    )
    first_name = models.CharField(
        max_length=150, verbose_name="имя пользователя", help_text="Введите имя"
    )
    last_name = models.CharField(
        max_length=150, verbose_name="фамилия пользователя", help_text="Введите фамилию"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class UserProduct(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Выберите товар",
        related_name='user_product'
    )

    class Meta:
        abstract = True


# class Favorite(UserProduct):
#
#     class Meta:
#         ordering = ["id"]
#         verbose_name = "Избранное"
#         verbose_name_plural = "Избранное"
#         constraints = [
#             models.UniqueConstraint(fields=["product", "user"], name="unique_favorite")
#         ]


class ShoppingCart(UserProduct):
    amount = models.IntegerField(verbose_name="Количество", default=0)

    class Meta:
        ordering = ["id"]
        verbose_name = "корзина"
        verbose_name_plural = "корзины"
