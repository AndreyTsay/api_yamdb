from django.urls import path, include
from rest_framework import routers

from api_yamdb.users.views import SignUpViewSet, TokenViewSet, UsersViewSet

router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUpViewSet.as_view(), name="signup"),
    path('auth/token/', TokenViewSet.as_view(), name="token"),
]

