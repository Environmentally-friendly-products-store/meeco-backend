# Generated by Django 4.1.5 on 2023-09-20 09:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0015_alter_product_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "article_number",
                    models.CharField(max_length=50, verbose_name="Артикул"),
                ),
                (
                    "address",
                    models.CharField(
                        help_text="Введите адрес доставки",
                        max_length=255,
                        verbose_name="Адрес доставки",
                    ),
                ),
                (
                    "order_total",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Сумма заказа",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        help_text="Укажите статус",
                        max_length=50,
                        null=True,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Введите комментарий",
                        null=True,
                        verbose_name="Комментарий заказчика",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        help_text="Укажите заказчика",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Заказчик",
                    ),
                ),
            ],
            options={
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        default=0,
                        help_text="Введите количество",
                        verbose_name="Количество",
                    ),
                ),
                (
                    "purchase_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Цена за единицу товара в заказе",
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="orders.order",
                        verbose_name="Заказ",
                    ),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт в составе заказа",
                "verbose_name_plural": "продукты в заказе",
                "ordering": ("order_id",),
            },
        ),
        migrations.AddConstraint(
            model_name="orderproduct",
            constraint=models.UniqueConstraint(
                fields=("order_id", "product_id", "purchase_price"),
                name="unique_product_in_order",
            ),
        ),
    ]
