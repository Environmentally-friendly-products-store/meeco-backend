from django.db import models

class Orders(models.Model):
    article_number = models.CharField(max_length=50)
    customer = models.ForeignKey(
        "User", 
        on_delete=models.CASCADE,
        related_name='orders',
    )
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price_total = models.FloatField()
    status = models.CharField(max_length=50)

class OrderProducts(models.Model):
    id integer [primary key]
    order_id integer
    product_id integer
    amount integer
    purchase_price integer

class DeliveryAddress(models.Model):
    id integer [primary key]
    owner string
    country string
    city string
    street string
    house string
    apartment string
