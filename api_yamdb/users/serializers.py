from rest_framework import serializers

from api_yamdb.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, validated_data):
        if validated_data == 'me':
            raise serializers.ValidationError('Такой username запрещен.')
        return validated_data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, unique=True,
                                     verbose_name='Никнейм пользователя')
    confirmation_code = serializers.CharField(max_length=4, default='0000',
                                              verbose_name="Код подтверждения")

    def validate(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        if user.confirmation_code != validated_data['confirmation_code']:
            raise serializers.ValidationError('Проблемы с регистрацией ')
        return validated_data


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, unique=True,
                                     verbose_name='Никнейм пользователя')
    email = serializers.EmailField(max_length=254, unique=True,
                                   verbose_name="Почта")

    def validate(self, validated_data):
        if validated_data == 'me':
            raise serializers.ValidationError('Такой username запрещен.')
        return validated_data
