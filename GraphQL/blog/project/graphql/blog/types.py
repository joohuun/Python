from graphene import ID, Boolean, Int, List, Node, String
from graphene_django import DjangoObjectType

from ...blog.dataloaders import ArticleFavoriteDataLoader
from ...blog import models
from ...core.mutations import AppResolverInfo
from ..user.types import Profile


article_loader = ArticleFavoriteDataLoader()


class ArticleNode(DjangoObjectType):
    author = Profile()
    favorited = Boolean()
    favorites_count = Int()

    class Meta:
        model = models.Article
        fields = "__all__"
        interfaces = (Node, )

    @staticmethod
    def resolve_favorited(root:models.Article, info: AppResolverInfo):
        user = info.context.user
        return article_loader.load((user, root)).get()["favorited"]

    @staticmethod
    def resolve_favorites_count(root: models.Article, info: AppResolverInfo):
        user = info.context.user

        return article_loader.load((user, root)).get()["favorites_count"]
