from django.db import models

from core.models import DiscountMixin, NameDescriptionModel, SlugMixin


class Event(NameDescriptionModel, SlugMixin, DiscountMixin):
    """Модель акций по скидкам."""

    date_start = models.DateField("Дата начала акции")
    date_end = models.DateField("Дата окончания акции")

    class Meta:
        ordering = ("name",)
        verbose_name = "акция"
        verbose_name_plural = "акции"
