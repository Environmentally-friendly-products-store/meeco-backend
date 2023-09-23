from django.db import models

from core.models import DiscountMixin, NameDescriptionModel, SlugMixin

from .validators import validate_dates


class Event(NameDescriptionModel, SlugMixin, DiscountMixin):
    """Модель акций по скидкам."""

    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="events/",
        verbose_name="картинка акции",
        help_text="Загрузите картинку акции",
    )
    date_start = models.DateField("Дата начала акции")
    date_end = models.DateField("Дата окончания акции")

    def clean(self):
        validate_dates(self)

    class Meta:
        ordering = ("name",)
        verbose_name = "акция"
        verbose_name_plural = "акции"
