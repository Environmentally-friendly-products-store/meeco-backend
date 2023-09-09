from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()


class Orders(models.Model):
    article_number = models.CharField(max_length=50)
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address = models.ForeignKey(
        "DeliveryAddress",
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price_total = models.FloatField()
    status = models.CharField(max_length=50)


class OrderProducts(models.Model):
    order_id = models.ForeignKey(
        Orders,
        on_delete=models.SET_NULL,
        related_name="orderProducts",
        null=True
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.FloatField()
    purchase_price = models.FloatField()


class DeliveryAddress(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deliveryAddress",
    )
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10)
