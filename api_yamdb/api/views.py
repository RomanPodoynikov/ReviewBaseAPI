from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
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
from api.mixins import PostGetDeleteViewSet
from api.pagination import Pagination
from api.permissions import Admin_Only, IsAdmin
from api.serializers import (CategorySerializer, ChangeMeForAuthUserSerializer,
                             CreateUserSerializer, GenreSerializer,
                             GetTokenSerializer, ReadTitleSerializer,
                             TitleSerializer, UsersSerializer)
from reviews.models import Category, Genre, Title
from user.models import User


class CreateUserView(APIView):
    """Представление создания юзера"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        try:
            user, create = User.objects.get_or_create(username=username,
                                                      email=email)
        except IntegrityError:
            return Response('Login или Email уже занят',
                            status=HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения регистрации',
            message='Используйте для получения токена\n'
                    f'confirmation_code:{confirmation_code}\n'
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
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Предоставляет пользователю JWT токен по коду подтверждения.
        """
        serializer = GetTokenSerializer(data=request.data)
        if not serializer.is_valid():
            message = 'Данные не валидны'
            return Response(message, status=HTTP_400_BAD_REQUEST)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = 'confirmation_code не совпадает'
            return Response(message, status=HTTP_400_BAD_REQUEST)
        user.save()
        message = {'token': str(AccessToken.for_user(user))}
        message = ('Успех', {'token': str(AccessToken.for_user(user))})
        return Response(message, status=HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, Admin_Only,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    pagination_class = Pagination
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options',
                         'trace', ]

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated], url_path='me')
    def user_get_or_patch_me(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_authenticated:
                serializer = ChangeMeForAuthUserSerializer(request.user,
                                                           data=request.data,
                                                           partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.data)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = Pagination
    filterset_fields = ('name', 'year', 'category', 'genre',)

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
    pagination_class = Pagination
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
    pagination_class = Pagination
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)
