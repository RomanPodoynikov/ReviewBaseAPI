from django.conf import settings
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        EmailField, ModelSerializer,
                                        Serializer, SerializerMethodField,
                                        EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField, ValidationError)
from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User

from api.mixins import UsernameValeidationMixin


class CreateUserSerializer(UsernameValeidationMixin, Serializer):
    """Сериализатор данных для создания пользователя."""
    email = EmailField(max_length=254, required=True)
    username = CharField(max_length=150, required=True)

    class Meta:
        fields = ('username', 'email')


class GetTokenSerializer(UsernameValeidationMixin, Serializer):
    """Сериализатор данных для создания токена."""
    username = CharField(max_length=150, required=True)
    confirmation_code = CharField(
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class UsersSerializer(ModelSerializer):
    """Сериализатор для модели User при обращении admin."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(UsersSerializer):
    """Сериализатор для модели User при обращении auth user."""

    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)


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


class PostPatchDeleteTitleSerializer(ModelSerializer):
    """
    Сериализатор для модели Title при использовании методов POST, PATCH,
    DELETE.
    """
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadTitleSerializer(ModelSerializer):
    """Сериализатор для модели Title при использовании метода GET."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )

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
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        exclude = ('review',)
