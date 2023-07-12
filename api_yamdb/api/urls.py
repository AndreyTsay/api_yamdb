
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api import views
from api.views import UsersViewSet, TokenViewSet, SignUpViewSet

router = SimpleRouter()

router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('titles', views.TitleViewSet)
router.register('users', UsersViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns_users = [
    path('auth/token/', TokenViewSet.as_view(), name="token"),
    path('auth/signup/', SignUpViewSet.as_view(), name="signup")
]
urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(urlpatterns_users)),
]
