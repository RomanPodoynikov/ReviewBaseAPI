
from rest_framework.serializers import (ModelSerializer,
                                        SlugRelatedField,
                                        SerializerMethodField,
                                        CharField,
                                        ValidationError,
                                        PrimaryKeyRelatedField,
                                        CurrentUserDefault)
from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from django.db.models import Avg


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class TitleSerializer(ModelSerializer):
    genre = SlugRelatedField(queryset=Genre.objects.all(),
                             slug_field='slug', many=True)
    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


class ReadTitleSerializer(ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField()

    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating", "description",
                  "genre", "category")

    def get_rating(self, obj):
        ob = get_object_or_404(Title, pk=obj.id)
        rating = ob.reviews.aggregate(Avg("score"))
        return rating['score__avg']


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True,
        default=CurrentUserDefault())
    title = PrimaryKeyRelatedField(
        queryset=Title.objects.all(), write_only=True)

    def to_internal_value(self, data):
        data['title'] = self.context['view'].get_title().id
        return super().to_internal_value(data)

    class Meta:
        model = Review
        fields = '__all__'

    # Невозможность написать более одного отзыва на произведение
    validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('author', 'title'),
            message='Вы уже оставляли отзыв на это произведение.',
        )
    ]


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True,
        default=CurrentUserDefault())
    review = PrimaryKeyRelatedField(
        queryset=Review.objects.all(), write_only=True)

    def to_internal_value(self, data):
        data['review'] = self.context['view'].get_review().id
        return super().to_internal_value(data)

    class Meta:
        model = Comment
        fields = '__all__'
