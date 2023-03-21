from rest_framework.serializers import (ModelSerializer,
                                        SlugRelatedField,
                                        SerializerMethodField)
from reviews.models import Category, Comment, Genre, Review, Title
# from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from django.db.models import Avg

class GenreSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
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
    # когда будет модель User, добавить ее и использовать это поле
    # author = SlugRelatedField(
    #     slug_field='username', read_only=True,
    #     default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    # проверить score, на уровне модели проверяется
    # def validate_rating(self, value):
    #     if value < 1 or value > 10:
    #         raise serializers.ValidationError('Rating has to be between 1 and 10.')
    #     return value

        # Невозможность написать более одного отзыва на произведение

        # протестировать, когда будет User. Описать title
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('author', 'title'),
        #         message='Вы уже оставляли отзыв на это произведение.',
        #     )
        # ]


class CommentSerializer(ModelSerializer):
    # когда будет модель User, добавить ее и использовать это поле
    # author = SlugRelatedField(
    #     slug_field='username', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


# Дописать в сериалайзер для Title
# импорт from rest_framework.serializers import SerializerMethodField
# from django.shortcuts import get_object_or_404
# from django.db.models import Avg
#     "rating" - должно быть среди filds
#     rating = SerializerMethodField()
#     def get_rating(self, obj):
#         ob = get_object_or_404(Title, pk=obj.id)
#         rating = ob.reviews.aggregate(Avg("score"))
#         return rating

# или to_representation()


