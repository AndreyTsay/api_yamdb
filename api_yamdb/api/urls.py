
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='сategories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]
