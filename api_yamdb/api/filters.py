from django_filters import FilterSet, ModelMultipleChoiceFilter

from reviews.models import Genre, Title


class TitleFilterSet(FilterSet):
    genre = ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        field_name='genre__slug',
        lookup_expr='in'
    )

    class Meta:
        model = Title
        fields = ['genre']
