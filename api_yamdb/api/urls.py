from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()

router.register('categoty', CategoryViewSet)
router.register('genre', GenreViewSet)
router.register('title', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
