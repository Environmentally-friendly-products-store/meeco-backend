# Generated by Django 4.1.5 on 2023-09-17 11:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ["id"],
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
            },
        ),
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(
                default=1, max_length=255, verbose_name="Адрес доставки"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="amount",
            field=models.IntegerField(default=0, verbose_name="Количество"),
        ),
        migrations.DeleteModel(
            name="DeliveryAddress",
        ),
    ]
