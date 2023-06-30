from django.urls import path

from api_yamdb.users.views import SignUpViewSet, TokenViewSet, UsersViewSet

urlpatterns = [
    path('signup/', SignUpViewSet.as_view(), name='signup'),
    path('token/', TokenViewSet.as_view(), name='token'),
    path('users/me/', UsersViewSet.as_view(), name='me'),
]
