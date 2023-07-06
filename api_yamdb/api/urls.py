
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UsersViewSet, SignUpViewSet


router = SimpleRouter()

router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UsersViewSet, basename='users')

urlpatterns_users = [
    path('auth/token/', TokenObtainPairView, name="token"),
    path('auth/signup/', SignUpViewSet, name="signup")
]
urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(urlpatterns_users)),
]
