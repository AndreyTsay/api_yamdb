from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAdminOrReadOnly, IsSuperUserOrIsAdminOnly


class GetPostDeleteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly or IsSuperUserOrIsAdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
