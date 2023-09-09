from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from events.models import Event
from users.models import User


class Product(models.Model):
    name = models.CharField(
        verbose_name='Название товара',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание товара',
        max_length=255
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория товара',

    )
    brand = models.ForeignKey(
        'Brand',
        verbose_name='Брэнд товара'
    )
    event = models.ForeignKey(
        Event,
        verbose_name='Событие'
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за штуку'
    )
    discount = models.IntegerField(
        verbose_name='Скидка в процентах',
        default=0,
        validators=[
            models.MinValueValidator(0),
            models.MaxValueValidator(100),
        ]
    )
    rating = models.DecimalField(
        verbose_name='Рейтинг товара',
        max_digits=3,
        decimal_places=2
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    view_amount = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        default=0
    )
    buy_amount = models.PositiveIntegerField(
        verbose_name='Количество покупок',
        default=0
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ImageSet(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = ProcessedImageField(
        upload_to='product_images/',
        verbose_name='Основное изображение'
    )
    big_image = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1000, 1000)],
        format='JPEG',
        options={'quality': 100}
    )
    preview_image = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80}
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 70}
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        default=1
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание категории',
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название бренда'
    )
    description = models.TextField(
        verbose_name='Описание бренда',
        max_length=255
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Страна бренда'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
