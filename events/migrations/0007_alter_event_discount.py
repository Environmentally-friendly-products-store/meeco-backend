# Generated by Django 4.1.5 on 2023-09-21 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0006_alter_event_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="discount",
            field=models.PositiveSmallIntegerField(
                blank=True,
                default=0,
                help_text="Введите целое число от 0 до 100",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "Скидка должна быть больше или равна нулю"
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
