# Generated by Django 4.1.5 on 2023-10-09 10:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
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
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=30,
                        verbose_name="Название",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Введите описание",
                        max_length=255,
                        verbose_name="Описание",
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
                (
                    "discount",
                    models.PositiveSmallIntegerField(
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
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите картинку акции",
                        null=True,
                        upload_to="events/",
                        verbose_name="картинка акции",
                    ),
                ),
                ("date_start", models.DateField(verbose_name="Дата начала акции")),
                ("date_end", models.DateField(verbose_name="Дата окончания акции")),
            ],
            options={
                "verbose_name": "акция",
                "verbose_name_plural": "акции",
                "ordering": ("name",),
            },
        ),
    ]
