from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
from orders import appvars as VARS

User = get_user_model()


class DeliveryAddress(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deliveryAddress",
    )
    country = models.CharField(max_length=VARS.DEL_ADDR_COUNTRY_ML)
    city = models.CharField(max_length=VARS.DEL_ADDR_CITY_ML)
    street = models.CharField(max_length=VARS.DEL_ADDR_STREET_ML)
    house = models.CharField(max_length=VARS.DEL_ADDR_HOUSE_ML)
    apartment = models.CharField(max_length=VARS.DEL_ADDR_APARTMENT_ML)

    class Meta:
        ordering = ("owner",)
        verbose_name = "адрес доставки"
        verbose_name_plural = "адреса доставки"

    def __str__(self):
        return self.country


class Order(models.Model):
    article_number = models.CharField(max_length=VARS.ORDER_ARTICLE_ML)
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price_total = models.FloatField()
    status = models.CharField(max_length=VARS.ORDER_STATUS_ML)
    comment = models.TextField()

    class Meta:
        ordering = ("customer",)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return self.article_number


class OrderProduct(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.SET_NULL, related_name="orderProducts", null=True
    )
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    purchase_price = models.FloatField()

    class Meta:
        ordering = ("order_id",)
        verbose_name = "продукт в составе заказа"
        verbose_name_plural = "продукты в заказе"
