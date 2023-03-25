from django.shortcuts import get_object_or_404, get_list_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Comment, Genre, Review, Title

from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, ReadTitleSerializer)
from api.pagination import TitlePagination
from api.filters import TitleFilter
from api.mixins import PostGetDeleteViewSet
from api.permissions import IsAdmin, IsOwnerOrModeratorOrReadOnly


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = TitlePagination
    filterset_fields = ('name', 'year', 'category', 'genre',)
    # permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return (IsAdmin(),)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleSerializer
        return ReadTitleSerializer


class GenreViewSet(PostGetDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    pagination_class = TitlePagination
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)


class CategoryViewSet(PostGetDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    pagination_class = TitlePagination
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)


class ReviewViewSet(ModelViewSet):
    """ViewSet для просмотра, создания и редактирования отзывов."""
    serializer_class = ReviewSerializer
    # permission_classes = (AllowAny, )
    permission_classes = (IsOwnerOrModeratorOrReadOnly,)

    def get_queryset(self):
        """Метод для определения queryset (отзывы только 1 произведения.)"""
        title_id = self.kwargs.get('title_id')
        reviews_queryset = get_object_or_404(Title, id=title_id).reviews
        # print(get_object_or_404(Title, id=title_id).reviews.all())
        # print(self.request.user)
        return reviews_queryset.all()

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_title(self, key='title_id'):
        return get_object_or_404(Title, id=self.kwargs.get(key))


class CommentViewSet(ModelViewSet):
    """ViewSet для просмотра, создания и редактирования
    комментариев к отзывам.
    """
    serializer_class = CommentSerializer
    # permission_classes = (AllowAny, )
    permission_classes = (IsOwnerOrModeratorOrReadOnly,)

    def get_queryset(self):
        """Метод для определения queryset (комментарии только 1 отзыва.)"""
        review_id, title_id = (self.kwargs.get('reviews_id'),
                               self.kwargs.get('title_id'))
        comments_queryset = get_object_or_404(
            Review, id=review_id, title=title_id).comments
        return comments_queryset.all()

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        review_id, title_id = (self.kwargs.get('reviews_id'),
                               self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_review(self, key='reviews_id'):
        return get_object_or_404(Review, id=self.kwargs.get(key))
