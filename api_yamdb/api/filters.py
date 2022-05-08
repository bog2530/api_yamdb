import django_filters

from reviews.models import Title


class TitleFilter(django_filters.rest_framework.FilterSet):
    genre = django_filters.CharFilter(lookup_expr='slug')
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='slug'
    )
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['year', 'name', 'category', 'genre']
