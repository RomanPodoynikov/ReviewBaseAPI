from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from user.models import User

from api.filters import TitleFilter
from api.mixins import PostGetDeleteViewSet
from api.pagination import Pagination
from api.permissions import IsAdmin, IsOwnerOrModeratorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateUserSerializer, GenreSerializer,
                             GetTokenSerializer, MeSerializer,
                             ReadTitleSerializer, ReviewSerializer,
                             TitleSerializer, UsersSerializer)
from api.permissions import (Admin_Only, IsOwnerOrPrivilegeduserOrReadOnly,
                             TitlePermission)
from api.serializers import (CategorySerializer, ChangeMeForAuthUserSerializer,
                             CommentSerializer, CreateUserSerializer,
                             GenreSerializer, GetTokenSerializer,
                             PostPatchDeleteTitleSerializer,
                             ReadTitleSerializer, ReviewSerializer,
                             UsersSerializer)
from api.utils import PostGetDeleteViewSet
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
        if User.objects.filter(username=username) or User.objects.filter(
            email=email
        ):
            if not User.objects.filter(username=username, email=email):
                return Response('Login или Email уже занят',
                                status=HTTP_400_BAD_REQUEST)
        user, create = User.objects.get_or_create(username=username,
                                                  email=email)
        user.save()
        send_mail(
            subject='Код подтверждения регистрации',
            message='Используйте для получения токена\n'
                    f'confirmation_code:'
                    '{default_token_generator.make_token(user)}\n'
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
        if User.objects.filter(username=request.data['username']):
            if serializer.is_valid():
                username = serializer.validated_data.get('username')
                confirmation_code = serializer.validated_data.get(
                    'confirmation_code'
                )
                user = User.objects.get(username=username)
                if not default_token_generator.check_token(
                    user, confirmation_code
                ):
                    message = (
                        'Отсутствует обязательное поле или оно некорректно'
                    )
                    return Response(message, status=HTTP_400_BAD_REQUEST)
                user.save()
                message = {'token': str(AccessToken.for_user(user))}
                return Response(message, status=HTTP_200_OK)
        message = 'Пользователь не найден'
        return Response(message, status=HTTP_404_NOT_FOUND)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username', )
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
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = PostPatchDeleteTitleSerializer
    permission_classes = (TitlePermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    filterset_fields = ('name', 'year', 'category', 'genre',)

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg(F("reviews__score")))

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostPatchDeleteTitleSerializer
        return ReadTitleSerializer


class GenreViewSet(PostGetDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (TitlePermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(PostGetDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (TitlePermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


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
        return self.kwargs.get('reviews_id')

    def get_title(self):
        """Метод для получения произведения."""
        return self.kwargs.get('title_id')

    def get_queryset(self):
        """Метод для определения queryset (комментарии только 1 отзыва.)"""
        comments_queryset = get_object_or_404(
            Review, id=self.get_review(), title=self.get_title()
        ).comments
        return comments_queryset.all()

    def perform_create(self, serializer):
        """Метод для добавления доп.инфо при создании нового комментария."""
        review = get_object_or_404(
            Review, id=self.get_review(), title=self.get_title()
        )
        serializer.save(author=self.request.user, review=review)
