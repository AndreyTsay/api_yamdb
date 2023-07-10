from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserSerializer, SignUpSerializer, TokenSerializer

EMAIL = "myemail@mail.ru"


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
            serializer = UserSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)


class SignUpViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get_or_create(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'])[0]
                confirmation_code = default_token_generator.make_token(user)
                send_mail("Код подтверждения:", f"{confirmation_code}", EMAIL,
                          [user.email])
                return Response(serializer.data, status=HTTP_200_OK)
            except Exception:
                return Response('Вы уже зарегистрированы!',
                                status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TokenViewSet(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    username=serializer.validated_data['username'])
            except User.DoesNotExist:
                return Response('Пользователь не найден!',
                                status=HTTP_404_NOT_FOUND)
            if serializer.validated_data['confirmation_code'] \
                    == user.confirmation_code:
                token = RefreshToken.for_user(user).access_token
                return Response(token, status=HTTP_201_CREATED)
            return Response('Неверный код подтверждения!',
                            status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
