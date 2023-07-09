import re

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150)
    # email = serializers.EmailField(max_length=254)

    def validate(self, validated_data):
        if 'username' in validated_data:
            if not re.match(r'[\w.@+-]+\Z', validated_data['username']):
                raise serializers.ValidationError('Такой username запрещен.')
        return validated_data

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
        lookup_field = ('username',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=4)

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
