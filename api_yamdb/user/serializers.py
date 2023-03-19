from rest_framework import serializers
import re
from user.models import User
from django.core.validators import RegexValidator


class CreateUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True,)
    # username = serializers.CharField(required=True)
 
    class Meta:
        model = User
        fields = ['username','email',]


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        # unique=False,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ['username','confirmation_code',]

class UsersViewSet(serializers.ModelSerializer): # какой сериалайз-ер и вьюст использовать
    username = serializers.CharField(
        # unique=False,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ['username','confirmation_code',]