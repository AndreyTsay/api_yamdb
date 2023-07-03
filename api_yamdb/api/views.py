from rest_framework import viewsets

from api.permissions import OwnerOrReadOnly
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (OwnerOrReadOnly)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (OwnerOrReadOnly)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (OwnerOrReadOnly)
