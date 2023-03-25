import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError((f'Username "{value}" is not valid.'),)


def MyReqularValidator(value):
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(('Username has not valid simbols.'),)
