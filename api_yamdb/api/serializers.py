import re

from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer, SlugRelatedField,
                                        ValidationError)
from reviews.models import Category, Genre, Title
from user.models import User


class CreateUserSerializer(Serializer):
    """Сериализатор данных для создания пользователя."""
    email = EmailField(max_length=254, required=True)
    username = CharField(max_length=150, required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError('Нельзя использовать логин me')
        elif not re.match(r'^[\w.@+-]+\Z', data['username']):
            raise ValidationError('Использованы недопустимые символы.')
        return data

    class Meta:
        fields = ('username', 'email')


class GetTokenSerializer(ModelSerializer):
    """Сериализатор данных для создания токена."""
    class Meta:
        model = User
        fields = ['username', 'confirmation_code', ]


class UsersSerializer(ModelSerializer):
    """Сериализатор для модели User при обращении admin."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class ChangeMeForAuthUserSerializer(ModelSerializer):
    """Сериализатор для модели User при обращении auth user."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        read_only_fields = ['role', ]


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class TitleSerializer(ModelSerializer):
    """
    Сериализатор для модели Title при использовании методов POST, PATCH,
    DELETE.
    """
    genre = SlugRelatedField(queryset=Genre.objects.all(),
                             slug_field='slug', many=True)
    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


class ReadTitleSerializer(ModelSerializer):
    """Сериализатор для модели Title при использовании метода GET."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
