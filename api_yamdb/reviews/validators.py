from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year_less_now(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} должен быть раньше, чем - {now}',
        )
