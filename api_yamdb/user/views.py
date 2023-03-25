from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User
from user.permissions import IsUserOrReadOnly
from user.serializers import CreateUserSerializer, GetTokenSerializer
from django.conf import settings


class CreateUserViewSet(viewsets.ViewSet):
    """
    Вьюсет создания нового пользователя,
    генерации confirmation code,
    отправки confirmation code  на указанный email
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            user = User.objects.create(username=username, email=email)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код подтверждения регистрации',
                message='Используйте для получения токена\n'
                        f'confirmation_code:{confirmation_code}\n'
                        f'username: {username}\n',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """
    Вьюсет для генерации JWT токена
    в обмен на confirmation_code и username.
    """
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Предоставляет пользователю JWT токен по коду подтверждения."""
        serializer = GetTokenSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            message = 'Данные не валидны' 
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = 'confirmation_code не совпадает'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        # это
        message = {'token': str(AccessToken.for_user(user))}
        # вместо этого
        # message = 'Активация успешно завершена'
        return Response(message, status=status.HTTP_200_OK)



class UsersViewSet(viewsets.ModelViewSet):
    """
    Получить список всех пользователей.
    Права доступа: Администратор
    """
    queryset = User.objects.all()
    # serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
