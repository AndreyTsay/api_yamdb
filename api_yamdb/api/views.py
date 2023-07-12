from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_200_OK)
from rest_framework.views import APIView

from api import serializers
from api.filters import TitleFilter
from api.mixins import GetPostDeleteViewSet
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsSuperUserOrIsAdminOnly,
                             IsSuperUserIsAdminIsModeratorIsAuthor)
from reviews.models import Category, Genre, Title, Review
from users.models import User

EMAIL = "myemail@mail.ru"


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (IsAdminOrReadOnly or IsSuperUserOrIsAdminOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=[IsAuthenticated, AllowAny],
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = serializers.UserSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)


class SignUpViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'])[0]
            confirmation_code = default_token_generator.make_token(user)
            send_mail("Код подтверждения:", f"{confirmation_code}", EMAIL,
                      [user.email])
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TokenViewSet(APIView):
    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = get_object_or_404(User, username=serializer.
                                     validated_data['username'])
            if (serializer.validated_data['confirmation_code']
                    == user.confirmation_code):
                token = RefreshToken.for_user(user).access_token
                return Response(token, status=HTTP_201_CREATED)
            return Response('Неверный код подтверждения!',
                            status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
