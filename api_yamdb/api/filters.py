from django_filters import FilterSet, filters

from reviews.models import Title


class TitleFilterSet(FilterSet):
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
