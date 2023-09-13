from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Event(models.Model):
    """Модель акций по скидкам."""
    name = models.CharField('название', max_length=50)
    description = models.CharField('описание', max_length=255)
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
    slug = models.SlugField('уникальный слаг', unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}{self.date_start}')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name = "акция"
        verbose_name_plural = "акции"

    def __str__(self):
        return self.name
