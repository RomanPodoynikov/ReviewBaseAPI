from rest_framework.viewsets import ModelViewSet

from reviews.models import Comment, Review   # Title
from .serializers import CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.


class ReviewViewSet(ModelViewSet):
    """ViewSet для просмотра, создания и редактирования отзывов."""
    serializer_class = ReviewSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Метод для определения queryset (отзывы только 1 произведения.)"""
        # использовать, когда будет модель Title,  удалить из импортов get_list_or_404
        # title_id = self.kwargs.get('title_id')
        # reviews_queryset = get_object_or_404(Title, id=title_id).reviews
        # return reviews_queryset
        title_id = self.kwargs.get('title_id')
        reviews_queryset = get_list_or_404(Review, title=title_id)
        return reviews_queryset

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        # использовать, когда будет модель Title
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

        # title_id = self.kwargs.get('title_id')
        # review_id = self.kwargs.get('review_id')
        # comments_queryset = get_object_or_404(
        #     Title, id=title_id).revievs.get(id=review_id).comments
        review_id = self.kwargs.get('review_id')
        comments_queryset = get_object_or_404(Review, id=review_id).comments
        return comments_queryset

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        review_id = self.kwargs.get('review_id')
        # тестировать только после модели Titles
        # title_id = self.kwargs.get('title_id')
        #  title = get_object_or_404(Title, id=title_id)
        # if title.reviews.filter(id__exact=review_id):
        
        serializer.save(author=self.request.user, review=review_id)
