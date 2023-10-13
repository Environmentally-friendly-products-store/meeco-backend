from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Sum

from core.models import CreatedAtMixin
from orders import appvars as VARS
from products.models import Product

User = get_user_model()


class Order(CreatedAtMixin):
    article_number = models.CharField(
        max_length=VARS.ORDER_ARTICLE_ML,
        verbose_name="Артикул",
        null=True,
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Заказчик",
        help_text="Укажите заказчика",
    )
    contact_phone_number = models.CharField(
        max_length=VARS.ORDER_PHONE_ML,
        verbose_name="Контактный номер телефона",
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=VARS.ORDER_ADDRESS_ML,
        verbose_name="Адрес доставки",
        help_text="Введите адрес доставки",
        null=True,
    )
    price_total = models.DecimalField(
        verbose_name="Сумма заказа",
        max_digits=VARS.ORDER_TOTAL_MDIGIT,
        decimal_places=VARS.ORDER_TOTAL_DECIMAL,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=VARS.ORDER_STATUS_ML,
        verbose_name="Статус",
        help_text="Укажите статус",
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name="Комментарий заказчика",
        help_text="Введите комментарий",
        blank=True,
        null=True,
    )
    products = models.ManyToManyField(Product, through="OrderProduct")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Order {self.id}"

    @property
    def products_count(self):
        return self.products.aggregate(Count("id"))["id__count"]

    @property
    def get_price_total(self):
        return Decimal(
            self.products.aggregate(total=Sum("order_products__item_total"))[
                "total"
            ]
        )

    def save(self, *args, **kwargs):
        self.price_total = self.get_price_total
        super().save(*args, **kwargs)


class OrderProduct(models.Model):
    """Вспомогательная модель, связывающая товары и заказы."""

    order_id = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="order_products",
        verbose_name="Заказ",
        null=True,
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="order_products",
        verbose_name="Товар",
        null=True,
    )
    amount = models.IntegerField(
        default=1,
        verbose_name="Количество",
        help_text="Введите количество",
    )
    purchase_price = models.DecimalField(
        verbose_name="Цена за единицу",
        max_digits=VARS.ORD_PROD_PRICE_MDIGIT,
        decimal_places=VARS.ORD_PROD_PRICE_DECIMAL,
        blank=True,
        null=True,
    )
    item_total = models.DecimalField(
        verbose_name="Стоимость позиции",
        max_digits=VARS.ORD_PROD_PRICE_MDIGIT,
        decimal_places=VARS.ORD_PROD_PRICE_DECIMAL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("product_id",)
        verbose_name = "продукт в составе заказа"
        verbose_name_plural = "продукты в заказе"
        constraints = [
            models.UniqueConstraint(
                fields=["order_id", "product_id", "purchase_price"],
                name="unique_product_in_order",
            )
        ]

    def __str__(self):
        return f"{self.id}"

    @property
    def get_item_total(self):
        return self.amount * self.purchase_price

    def save(self, *args, **kwargs):
        self.item_total = self.get_item_total
        super().save(*args, **kwargs)
