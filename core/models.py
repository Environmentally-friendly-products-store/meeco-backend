from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class NameDescriptionModel(models.Model):
    name = models.CharField(
        max_length=30, verbose_name="Название", help_text="Введите название"
    )
    description = models.TextField(
        max_length=255, verbose_name="Описание", help_text="Введите описание"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, verbose_name="Слаг")

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        abstract = True


class DiscountMixin(models.Model):
    discount = models.PositiveSmallIntegerField(
        "cкидка",
        blank=True,
        default=0,
        help_text="Введите целое число от 0 до 100",
        validators=[
            MinValueValidator(
                settings.MIN_DISCOUNT, "Скидка должна быть больше или равна нулю"
            ),
            MaxValueValidator(
                settings.MAX_DISCOUNT,
                f"Скидка не должна превышать\
                                  {settings.MAX_DISCOUNT} %.",
            ),
        ],
    )

    class Meta:
        abstract = True
