import re

from rest_framework import serializers

import reviews.models
from rest_framework.validators import UniqueValidator

from users.models import User

from users.validators import validate_me


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = reviews.models.Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = reviews.models.Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        fields = '__all__'
        model = reviews.models.Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = reviews.models.Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=reviews.models.Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=reviews.models.Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = reviews.models.Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        model = reviews.models.Review
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']
        extra_kwargs = {
            'title': {'required': False},
            'count': {'required': False},
        }


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = reviews.models.Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, required=True,
        validators=[validate_me,
                    UniqueValidator(queryset=User.objects.all()), ])

    email = serializers.EmailField(max_length=254, required=True,
                                   validators=[UniqueValidator]
                                   )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, validated_data):
        if 'username' in validated_data:
            if not re.match(r'[\w.@+-]+\Z', validated_data['username']):
                raise serializers.ValidationError('Такой username запрещен.')
        return validated_data

    def validate_email(self, validated_data):
        if User.objects.filter(email=validated_data).exists():
            raise serializers.ValidationError(
                'Аккаунт с таким email уже существует.'
            )
        return validated_data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, validated_data):
        if validated_data['username'] == 'me' or \
                not re.match(r'[\w.@+-]+\Z', validated_data['username']):
            raise serializers.ValidationError('Такой username запрещен.')
        return validated_data
