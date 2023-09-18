from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from core.models import CreatedAtMixin
from orders import appvars as VARS
from products.models import Product

User = get_user_model()


# class DeliveryAddress(models.Model):
#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="deliveryAddress",
#     )
#     country = models.CharField(max_length=VARS.DEL_ADDR_COUNTRY_ML)
#     city = models.CharField(max_length=VARS.DEL_ADDR_CITY_ML)
#     street = models.CharField(max_length=VARS.DEL_ADDR_STREET_ML)
#     house = models.CharField(max_length=VARS.DEL_ADDR_HOUSE_ML)
#     apartment = models.CharField(max_length=VARS.DEL_ADDR_APARTMENT_ML)


class Order(CreatedAtMixin):
    article_number = models.CharField(
        max_length=VARS.ORDERS_ARTICLE_ML, verbose_name="Артикул"
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Заказчик",
        help_text="Укажите заказчика",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес доставки",
        help_text="Введите адрес доставки",
    )
    # address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    price_total = models.FloatField(
        verbose_name="Цена заказа",
    )
    status = models.CharField(
        max_length=VARS.ORDERS_STATUS_ML,
        verbose_name="Статус",
        help_text="Укажите статус",
    )
    comment = models.TextField(
        verbose_name="Комментарий заказчика", help_text="Введите комментарий"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class OrderProduct(models.Model):
    """Вспомогательная модель, связывающая продукцию и заказы."""

    order_id = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="orderProducts",
        null=True,
        verbose_name="Заказ",
    )
    product_id = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, verbose_name="Товар"
    )
    amount = models.IntegerField(
        default=0,
        verbose_name="Количество",
        help_text="Введите количество",
    )
    purchase_price = models.FloatField(
        verbose_name="Цена за единицу товара в заказе",
    )

    class Meta:
        verbose_name = "продукт в заказе"
        verbose_name_plural = "продукты в заказе"
        UniqueConstraint(fields=["product", "order"], name="unique_product_event")
