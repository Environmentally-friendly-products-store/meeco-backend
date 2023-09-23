from django.core.exceptions import ValidationError


def validate_dates(value):
    date_start = value.date_start
    date_end = value.date_end
    if date_start and date_end and date_start >= date_end:
        raise ValidationError("Дата окончания должна быть позже даты начала акции.")
