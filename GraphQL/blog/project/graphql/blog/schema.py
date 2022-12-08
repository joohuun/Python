import graphene_django_optimizer as gql_optimizer

from django.db.models.query import QuerySet
from graphene import Field, ObjectType, String
from graphene_django.filter import DjangoFilterConnectionField


from ...core.mutations import AppResolverInfo
from ...blog.filters import ArticleFilterSet
from ...blog import models
from ..blog.types import ArticleNode

class ArticleQueries(ObjectType):
    articles = DjangoFilterConnectionField(ArticleNode, filterset_class=ArticleFilterSet)
    get_article = Field(ArticleNode, slug=String(required=True))


    @staticmethod
    def resolve_articles(root, info: AppResolverInfo, **fields):
        return gql_optimizer.query(models.Article.objects.all(), info, disable_abort_only=True)

    @staticmethod
    def resolve_get_article(root, info: AppResolverInfo, **fields):
        optimized_query = gql_optimizer.query(
            models.Article.objects.filter(slug=fields.get("slug")),
            info,
            disable_abort_only=True,
        )
        return optimized_query.first()