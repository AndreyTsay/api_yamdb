from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import SignUpViewSet, UsersViewSet

router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('api/v1', include(router.urls)),
    path('api/v1/auth/signup/', SignUpViewSet.as_view(), name="signup"),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name="token"),
]
