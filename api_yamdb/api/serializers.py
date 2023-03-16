from rest_framework.serializers import ModelSerializer
from reviews.models import Category, Genre, Title


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class TitleSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
