# Generated by Django 4.1.5 on 2023-10-18 20:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                    "country",
                    models.CharField(
                        max_length=30, verbose_name="Страна происхождения бренда"
                    ),
                ),
            ],
            options={
                "verbose_name": "бренд",
                "verbose_name_plural": "бренды",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Category",
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
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
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
                    "price_per_unit",
                    models.FloatField(
                        help_text="Введите цену за единицу",
                        verbose_name="Цена за штуку",
                    ),
                ),
                (
                    "view_amount",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
                (
                    "buy_amount",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество покупок"
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        help_text="Введите производителя",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brand",
                        to="products.brand",
                        verbose_name="Брэнд",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Введите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category",
                        to="products.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        help_text="Введите промоакцию",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="events.event",
                        verbose_name="Акция",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ImageSet",
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
                    "image",
                    imagekit.models.fields.ProcessedImageField(
                        help_text="Загрузите изображение",
                        upload_to="product_images/",
                        verbose_name="Основное изображение",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Введите товар",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение к товару",
                "verbose_name_plural": "изображения к товарам",
                "ordering": ["id"],
            },
        ),
    ]
