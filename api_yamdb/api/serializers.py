import re

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        EmailField, ModelSerializer,
                                        Serializer,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)

from reviews.models import Category, Comment, Genre, Review, Title
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
    rating = SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')

    def get_rating(self, obj):
        ob = get_object_or_404(Title, pk=obj.id)
        rating = ob.reviews.aggregate(Avg("score"))
        return rating['score__avg']


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=CurrentUserDefault())
    title = SlugRelatedField(slug_field='name', read_only=True)

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв на это произведение.',
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True,
        default=CurrentUserDefault())

    class Meta:
        model = Comment
        exclude = ('review',)
