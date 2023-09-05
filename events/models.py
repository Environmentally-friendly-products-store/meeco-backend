from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint
from orders.models import Product


class Event(models.Model):
    """Модель акций по скидкам."""
    name = models.CharField('название', max_length=200)
    description = models.CharField('описание', max_length=200)
    discount = models.PositiveSmallIntegerField(
        'cкидка',
        help_text='Введите целое число от 1 до 100',
        validators=[
            MinValueValidator(settings.MIN_DISCOUNT,
                              'Скидка должна быть больше нуля'),
            MaxValueValidator(settings.MAX_DISCOUNT,
                              f'Скидка не должна превышать\
                              {settings.MAX_DISCOUNT} %.')]
    )
    date_start = models.DateField('Дата начала акции')
    date_end = models.DateField('Дата окончания акции')

    class Meta:
        ordering = ("name",)
        verbose_name = "акция"
        verbose_name_plural = "акции"

    def __str__(self):
        return self.name


class ProductEvent(models.Model):
    """Вспомогательная модель, связывающая продукцию и акции."""
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_event')
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE,
                              verbose_name="акция",)

    class Meta:
        verbose_name = "акция продукта"
        verbose_name_plural = "акции продукции"
        UniqueConstraint(fields=['product', 'event'],
                         name='unique_product_event')
