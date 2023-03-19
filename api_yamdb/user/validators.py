from django.core.exceptions import ValidationError

def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            (f'Username "{value}" is not valid.'),
            params={'value': value},
        )