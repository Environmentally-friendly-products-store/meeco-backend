# Generated by Django 4.1.5 on 2023-10-18 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("orders", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                help_text="Укажите заказчика",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Заказчик",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                through="orders.OrderProduct", to="products.product"
            ),
        ),
        migrations.AddConstraint(
            model_name="orderproduct",
            constraint=models.UniqueConstraint(
                fields=("order_id", "product_id", "purchase_price"),
                name="unique_product_in_order",
            ),
        ),
    ]
