from rest_framework.serializers import ModelSerializer
from reviews.models import Comment, Review
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(ModelSerializer):
    # когда будет модель User, добавить ее и использовать это поле
    # author = SlugRelatedField(
    #     slug_field='username', read_only=True,
    #     default=serializers.CurrentUserDefault())


    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

        # Невозможность написать более одного отзыва на произведение

        # протестировать
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