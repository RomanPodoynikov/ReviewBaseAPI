import re

from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsAuthenticatedAndAdminOrSuperuserOrReadOnly


class GenreCategoryViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                           GenericViewSet):
    permission_classes = (IsAuthenticatedAndAdminOrSuperuserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UsernameValeidationMixin:
    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Нельзя использовать логин me')
        elif not re.match(r'^[\w.@+-]+\Z', username):
            raise ValidationError('Использованы недопустимые символы.')
        return username
