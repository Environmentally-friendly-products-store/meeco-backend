from django.contrib.auth import get_user_model
from django.db import models

from orders import appvars as VARS
from products.models import Product

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


class Order(models.Model):
    article_number = models.CharField(max_length=VARS.ORDERS_ARTICLE_ML)
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price_total = models.FloatField()
    status = models.CharField(max_length=VARS.ORDERS_STATUS_ML)
    comment = models.TextField()


class OrderProduct(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.SET_NULL, related_name="orderProducts", null=True
    )
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    purchase_price = models.FloatField()
