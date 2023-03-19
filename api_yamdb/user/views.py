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
        message = 'Активация успешно завершена'
        return Response(message, status=status.HTTP_200_OK)


# class UsersViewSet((mixins.CreateModelMixin,
#                     mixins.ListModelMixin,
#                     mixins.RetrieveModelMixin,
#                     viewsets.GenericViewSet):
class UsersViewSet(viewsets.ModelViewSet):
    """
    Получить список всех пользователей.
    Права доступа: Администратор
    """
    queryset = User.objects.all()
    # serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

# class CreateUserView(CreateAPIView):
#    queryset = User.objects.all() queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

#     (self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         username = request.data.get('username')
#         email = request.data.get('email')
#         user = get_object_or_404(User, username=username)
#         code = default_token_generator.make_token(user)

#         send_mail(
#             subject='Ваш код аутентификации',
#             message='Сохраните код! Он понадобится вам для получения токена.\n'
#                     f'confirmation_code:\n{code}\n'
#                     f'username: {username}',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[email],
#             fail_silently=False,
#         )

#         return Response(serializer.data, status=status.HTTP_201_CREATED,
#                         headers=headers)
      
      
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_token(request):
#     email = request.data.get('email')
#     user = get_object_or_404(User, email=email)
#     code = request.data.get('confirmation_code')
#     if default_token_generator.check_token(user, code):
#         user.is_active = True
#         user.save()
#         return Response({"message": "Аккаунт активирован"}, status.HTTP_200_OK)

#     return Response({"message": "неверный код подтверждения."},
#                     status.HTTP_400_BAD_REQUEST)