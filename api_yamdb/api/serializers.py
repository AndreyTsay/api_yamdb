from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import reviews.models
from api.validators import validate_username
from users.models import User


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

    def validate(self, data):
        if reviews.models.Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError('Отзыв уже оставлен!')
        return data

    class Meta:
        model = reviews.models.Review
        read_only_fields = ('title', 'author')
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
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all()), ])

    email = serializers.EmailField(max_length=254, required=True,
                                   validators=[UniqueValidator])

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
    username = serializers.CharField(max_length=150,
                                     validators=[validate_username, ])
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, validated_data):
        if User.objects.filter(username=validated_data['username'],
                               email=validated_data['email']).exists():
            return validated_data
        if (User.objects.filter(username=validated_data['username']).exists()
                or User.objects.filter(
                    email=validated_data['email']).exists()):
            raise serializers.ValidationError(
                'Вы уже зарегистрированы!'
            )
        return validated_data
