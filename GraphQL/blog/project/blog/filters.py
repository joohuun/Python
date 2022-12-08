from django.db.models import QuerySet
from django_filters import CharFilter, FilterSet
from ..blog import models

class ArticleFilterSet(FilterSet):
    tag = CharFilter(method="filter_tags")
    author_name = CharFilter("author__username")

    class Meta:
        model = models.Article
        fields = ("slug", "title")

    def filter_tags(
        self, query: QuerySet["models.Article"], *, value: str
    ) -> QuerySet["models.Article"]:
        return query.filter(tags__contains=[value])