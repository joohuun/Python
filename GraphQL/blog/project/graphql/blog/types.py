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


class CommentNode(DjangoObjectType):
    class Meta:
        model = models.Comment
        exclude = ()
        interfaces = (Node, )

        


###############
# Input Type  #
###############

class ArticleCreateInputType:
    title = String(required=True)
    slug = String(required=True)
    description =String(required=True)
    body = String(required=True)
    tags = List(String)


class ArticleUpdateInputType:
    slug = String(required=True)
    title = String()
    description = String()    
    body = String()

class ArticleDeleteInputType:
    slug = String(requried=True)


class CommentCreateInputType:
    body = String(required=True)
    article_slug = String(required=True)


class CommentUpdateInputType:
    comment_id = ID(requried=True)
    body = String(required=True)


class CommentDeleteInputType:
    comment_id = ID(requried=True)


class FavoriteInputType:
    article_slug = String(required=True)