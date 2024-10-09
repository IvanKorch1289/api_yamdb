from rest_framework import filters, mixins, viewsets

from api.permissions import IsAnonim, IsAdminOrReadOnly


class CreateUpdateDestroyViewset(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    """Базовый вьюсет без методов PATCH и GET по ID."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (IsAnonim, IsAdminOrReadOnly)
    lookup_field = 'slug'
