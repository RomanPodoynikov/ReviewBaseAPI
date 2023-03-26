import re

from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet


class PostGetDeleteViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                           GenericViewSet):
    pass


class UsernameValeidationMixin:
    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Нельзя использовать логин me')
        elif not re.match(r'^[\w.@+-]+\Z', username):
            raise ValidationError('Использованы недопустимые символы.')
        return username
