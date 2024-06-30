import django_filters

from django.contrib.postgres.search import SearchVector

from library_system.models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "language": ["exact"],
            "authors": ["exact"],
            "categories": ["exact"],
            "publication": ["exact"],
            "publish_date": ["lte", "gte"],
        }

    SEARCH_VECTOR = SearchVector(
        "title",
        "isbn",
        "summary",
        "authors__first_name",
        "authors__last_name",
        "categories__name",
        "publication__name",
    )

    search = django_filters.CharFilter(label="Search", method="filter_search")

    def filter_search(self, queryset, name, value):
        queryset = queryset.annotate(search=self.SEARCH_VECTOR)
        return queryset.filter(search=value)
