import graphene_django_optimizer as gql_optimizer

from django.db.models.query import QuerySet
from graphene import Field, ObjectType, String
from graphene_django.filter import DjangoFilterConnectionField


from ...core.mutations import AppResolverInfo
from ...blog.filters import ArticleFilterSet
from ...blog import models
from ..blog.types import ArticleNode
from .mutations import (
    CreateArticleMutation,
    DeleteArticleMutation,
    UpdateArticleMutation,
    FavoriteArticleMutation,
    CreateCommentMutation,
    DeleteCommentMutation,
    UpdateCommentMutation,

)

class ArticleQueries(ObjectType):
    articles = DjangoFilterConnectionField(ArticleNode, filterset_class=ArticleFilterSet)
    get_article = Field(ArticleNode, slug=String(required=True))


    @staticmethod
    def resolve_articles(root, info: AppResolverInfo):
        return gql_optimizer.query(models.Article.objects.all(), info, disable_abort_only=True)

    @staticmethod
    def resolve_get_article(root, info: AppResolverInfo, **data):
        optimized_query = gql_optimizer.query(
            models.Article.objects.filter(slug=data.get("slug")),
            info,
            # disable_abort_only=True,
        )
        return optimized_query.first()



class ArticleMutation(ObjectType):
    create_article = CreateArticleMutation.Field()
    delete_article = DeleteArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
    favorite_article = FavoriteArticleMutation.Field()
    create_comment = CreateCommentMutation.Field()
    delete_comment = DeleteCommentMutation.Field()
    update_comment = UpdateCommentMutation.Field()