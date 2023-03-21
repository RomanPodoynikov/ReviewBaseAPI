from django.shortcuts import get_object_or_404, get_list_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Comment, Genre, Review, Title

from api.mixins import PostGetDeleteViewSet
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, ReadTitleSerializer)


# Create your views here.


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = TitleFilter
    # pagination_class = TitlePagination
    filterset_fields = ('name', 'year', 'category', 'genre',)

    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return (AllowAny(),)
    #     return (IsAdmin(),)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleSerializer
        return ReadTitleSerializer




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


class ReviewViewSet(ModelViewSet):
    """ViewSet для просмотра, создания и редактирования отзывов."""
    serializer_class = ReviewSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Метод для определения queryset (отзывы только 1 произведения.)"""
        title_id = self.kwargs.get('title_id')
        reviews_queryset = get_object_or_404(Title, id=title_id).reviews
        return reviews_queryset

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=5, title=title)
        # использовать, когда будет модель User
        # title_id = self.kwargs.get('title_id')
        # title = get_object_or_404(Title, id=title_id)
        # serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """ViewSet для просмотра, создания и редактирования
    комментариев к отзывам.
    """
    serializer_class = CommentSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Метод для определения queryset (комментарии только 1 отзыва.)"""
        review_id, title_id = (self.kwargs.get('reviews_id'),
                               self.kwargs.get('title_id'))
        comments_queryset = get_object_or_404(
            Review, id=review_id, title=title_id).comments
        return comments_queryset

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        review_id, title_id = (self.kwargs.get('reviews_id'),
                               self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=1, review=review)
        # Использовать, когда будет модель User
        # serializer.save(author=self.request.user, review=review)

