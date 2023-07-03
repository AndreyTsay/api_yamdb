from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from api_yamdb.users import permissions
from api_yamdb.users.models import User
from api_yamdb.users.serializers import UserSerializer, SignUpSerializer
EMAIL = "myemail@mail.ru"


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdmin,)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=("GET", "PATCH"),
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(request.user, data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SignUpViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail("Код подтверждения:", f"{confirmation_code}", EMAIL,
                      [user.email])
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
