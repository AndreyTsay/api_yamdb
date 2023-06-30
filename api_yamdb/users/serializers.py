from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb.users.models import User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
