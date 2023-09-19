# Generated by Django 4.1.5 on 2023-09-17 16:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0011_alter_product_price_per_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Введите целое число от 1 до 100",
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "Скидка должна быть больше нуля"
                    ),
                    django.core.validators.MaxValueValidator(
                        100,
                        "Скидка не должна превышать                                  100 %.",
                    ),
                ],
                verbose_name="cкидка",
            ),
        ),
    ]
