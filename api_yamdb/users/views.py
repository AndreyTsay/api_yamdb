from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from api_yamdb.users import permissions
from api_yamdb.users.models import User
from api_yamdb.users.serializers import UserSerializer, SignUpSerializer, \
    TokenSerializer


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdmin,)
    pagination_class = LimitOffsetPagination


class SignUpViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer
    pagination_class = LimitOffsetPagination


class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer

