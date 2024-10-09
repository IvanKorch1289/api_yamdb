from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class CreateUpdateDestroyViewset(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    """Базовый вьюсет без методов PATCH и GET по ID."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'
