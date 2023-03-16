from django.core.exceptions import ValidationError

def validate_username(value):
    if value == 'me':
        raise ValidationError(
            (f'Имя пользователя не может быть {value}.'),
            params={'value': value},
        )