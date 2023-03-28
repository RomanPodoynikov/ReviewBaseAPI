from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAuthenticatedAndAdminOrReadOnly,
                             IsOwnerOrPrivilegeduserOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateUserSerializer, GenreSerializer,
                             GetTokenSerializer, MeSerializer,
                             ModificationTitleSerializer, ReadTitleSerializer,
                             ReviewSerializer, UsersSerializer)
from api.utils import GenreCategoryViewSet
from reviews.models import Category, Genre, Review, Title
from user.models import User


class CreateUserView(APIView):
    """Представление создания юзера"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        if User.objects.filter(username=username).first() != (
            User.objects.filter(email=email).first()
        ):
            return Response(
                'Login или Email уже занят',
                status=HTTP_400_BAD_REQUEST,
            )
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        send_mail(
            subject='Код подтверждения регистрации',
            message='Используйте для получения токена\n'
                    f'confirmation_code:'
                    f'{default_token_generator.make_token(user)}\n'
                    f'username: {username}\n',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=HTTP_200_OK)


class CreateTokenView(APIView):
    """
    Представление для генерации JWT токена в обмен на confirmation_code и
    username.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Предоставляет пользователю JWT токен по коду подтверждения.
        """
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])
        confirmation_code = serializer.validated_data.get(
            'confirmation_code',
        )
        if not default_token_generator.check_token(
            user,
            confirmation_code,
        ):
            message = (
                'Отсутствует обязательное поле или оно некорректно',
            )
            return Response(message, status=HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def user_get_or_patch_me(self, request):
        if request.method == 'GET':
            serializer = UsersSerializer(request.user)
            return Response(serializer.data)
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg(F("reviews__score"))).order_by("name")
    serializer_class = ModificationTitleSerializer
    permission_classes = (IsAuthenticatedAndAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('name', 'year', 'category', 'genre',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return ModificationTitleSerializer


class GenreViewSet(GenreCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    """ViewSet для просмотра, создания и редактирования отзывов."""
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsOwnerOrPrivilegeduserOrReadOnly,)

    def get_queryset(self):
        """Метод для определения queryset (отзывы только 1 произведения)."""
        title_id = self.kwargs.get('title_id')
        reviews_queryset = get_object_or_404(Title, id=title_id).reviews
        return reviews_queryset.all()

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """
    ViewSet для просмотра, создания и редактирования
    комментариев к отзывам.
    """
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsOwnerOrPrivilegeduserOrReadOnly,)

    def get_review(self):
        """Метод для получения ревью."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get('reviews_id'),
            title=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        """Метод для определения queryset (комментарии только 1 отзыва.)"""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        serializer.save(author=self.request.user, review=self.get_review())
