from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Genre, Title

from api.mixins import PostGetDeleteViewSet
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class GenreViewSet(PostGetDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(PostGetDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
