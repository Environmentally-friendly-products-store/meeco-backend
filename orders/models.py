from django.db import models


class Orders(models.Model):
    article_number = models.CharField(max_length=50)
    customer = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address = models.ForeignKey(
        "DeliveryAddress",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price_total = models.FloatField()
    status = models.CharField(max_length=50)


class OrderProducts(models.Model):
    order_id = models.ForeignKey(
        Orders,
        on_delete=models.SET_NULL,
        related_name="orderProducts",
    )
    product_id = models.ForeignKey(
        "Products",
        on_delete=models.SET_NULL,
    )
    amount = models.FloatField()
    purchase_price = models.FloatField()


class DeliveryAddress(models.Model):
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="deliveryAddress",
    )
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10)
