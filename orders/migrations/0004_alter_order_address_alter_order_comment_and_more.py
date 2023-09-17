# Generated by Django 4.1.5 on 2023-09-17 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0003_alter_orderproduct_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(
                help_text="Введите адрес доставки",
                max_length=255,
                verbose_name="Адрес доставки",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.TextField(
                help_text="Введите комментарий", verbose_name="Комментарий заказчика"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Заказчик",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="price_total",
            field=models.FloatField(verbose_name="Цена заказа"),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                help_text="Укажите статус", max_length=50, verbose_name="Статус"
            ),
        ),
    ]
