from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from users.models import User
from users.serializers import UserSerializer, SignUpSerializer

from users.serializers import TokenSerializer

from users.permissions import IsAdmin

EMAIL = "myemail@mail.ru"


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=[IsAuthenticated, ],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=HTTP_200_OK)
        serializer = UserSerializer(request.user, data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SignUpViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny, ]

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


class TokenViewSet(TokenViewBase):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)
