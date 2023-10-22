from django.contrib.auth.models import AbstractUser
from django.db import models

from products.models import Product

from .managers import MyUserManager


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="email",
        help_text="Введите email",
    )
    username = models.CharField(
        max_length=50, verbose_name="логин", help_text="Введите логин"
    )
    first_name = models.CharField(
        max_length=32, verbose_name="имя пользователя", help_text="Введите имя"
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name="фамилия пользователя",
        help_text="Введите фамилию",
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="телефон пользователя",
        help_text="Введите телефон",
    )

    class Meta:
        ordering = ["email"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class UserMixin(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )

    class Meta:
        abstract = True


class DeliveryAddress(UserMixin):
    city = models.CharField(
        max_length=100,
        verbose_name="город",
        help_text="Введите город",
    )
    street = models.CharField(
        max_length=150,
        verbose_name="улица",
        help_text="Введите улицу",
    )
    house = models.CharField(
        max_length=10,
        verbose_name="дом",
        help_text="Введите дом",
    )
    apartment = models.CharField(
        max_length=10,
        verbose_name="квартира",
        help_text="Введите квартиру",
    )

    class Meta:
        ordering = ["user"]
        verbose_name = "Адрес доставки"
        verbose_name_plural = "адреса доставки"


class Favorite(UserMixin):
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Выберите товар",
        related_name="favorite_product",
    )

    class Meta:
        ordering = ["user"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=["product", "user"], name="unique_favorite")
        ]


class ShoppingCart(UserMixin):
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Выберите товар",
        related_name="shopping_cart_product",
    )
    amount = models.PositiveSmallIntegerField(verbose_name="Количество", default=0)

    class Meta:
        ordering = ["user"]
        verbose_name = "корзина"
        verbose_name_plural = "корзины"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"], name="unique_shopping_cart"
            )
        ]
