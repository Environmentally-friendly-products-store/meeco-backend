from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

from core.models import (CreatedAtMixin, DiscountMixin, NameDescriptionModel,
                         SlugMixin)
from events.models import Event


class Product(NameDescriptionModel, DiscountMixin, CreatedAtMixin):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        help_text="Введите категорию",
        related_name="category",
    )
    brand = models.CharField(
        max_length=100, verbose_name="Брэнд", help_text="Введите производителя"
    )
    # brand = models.ForeignKey(
    #     "Brand", verbose_name="Брэнд", on_delete=models.CASCADE
    # )
    event = models.ForeignKey(
        Event,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Акция",
        help_text="Введите промоакцию",
    )
    price_per_unit = models.FloatField(
        verbose_name="Цена за штуку",
        help_text="Введите цену за единицу",
    )
    # rating = models.DecimalField(
    #     verbose_name="Рейтинг товара", max_digits=3, decimal_places=2
    # )
    view_amount = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    buy_amount = models.PositiveIntegerField(
        default=0, verbose_name="Количество покупок"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ImageSet(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар",
        help_text="Введите товар",
    )
    image = ProcessedImageField(
        upload_to="product_images/",
        verbose_name="Основное изображение",
        help_text="Загрузите изображение",
    )
    big_image = ImageSpecField(
        source="image",
        processors=[ResizeToFill(1000, 1000)],
        format="JPEG",
        options={"quality": 100},
    )
    preview_image = ImageSpecField(
        source="image",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 80},
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 70},
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "изображение к товару"
        verbose_name_plural = "изображения к товарам"


class Category(NameDescriptionModel, SlugMixin):
    class Meta:
        ordering = ["id"]
        verbose_name = "категория"
        verbose_name_plural = "категории"


# class Brand(NameDescriptionModel):
#     country = models.CharField(max_length=50, verbose_name="Страна бренда")
#     slug = models.SlugField(unique=True, verbose_name="Слаг")
#
#     class Meta:
#         ordering = ["id"]
#         verbose_name = "Бренд"
#         verbose_name_plural = "Бренды"
