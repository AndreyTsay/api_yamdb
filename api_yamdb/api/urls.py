
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from api import views
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UsersViewSet, SignUpViewSet


router = SimpleRouter()

router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('titles', views.TitleViewSet)
router.register('users', UsersViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    views.CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/\
        (?P<comment_id>\d+)/comment', views.CommentViewSet, basename='comment'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)
urlpatterns_users = [
    path('auth/token/', TokenObtainPairView, name="token"),
    path('auth/signup/', SignUpViewSet, name="signup")
]
urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(urlpatterns_users)),
]
