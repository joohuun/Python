import graphene
from ...account import models
from ...article import models

from graphql_auth import mutations
# from article.types import ArticleType
from .types import ArticleType, CommentType, LikeType
from .mutations import (
    CreateArticle,
    UpdateArticle, 
    DeleteArticle, 
    LikeArticle, 
    CreateComment,
    UpdateCommet,
    DeleteComment,
)
from graphql_auth.schema import MeQuery

from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

class ArticleQueries(MeQuery, graphene.ObjectType):
    all_articles = graphene.List(ArticleType)
    article_detail = graphene.Field(
        ArticleType,
        id = graphene.Argument(graphene.ID, required=True)
    )
    comment = graphene.List(CommentType, id=graphene.Int())
    like = graphene.List(LikeType, id=graphene.Int())



    def resolve_all_articles(self, info):
        return models.Article.objects.all()

    def resolve_article_detail(self, info, id):
        return models.Article.objects.get(pk=id)

    def resolve_comment(self, info, id):
        return models.Comment.objects.get(pk=id)

    def resolve_like(self, info, id):
        return models.Like.objects.get(pk=id)

    

class ArticleMutation(graphene.ObjectType):
    create_article = CreateArticle.Field()
    update_aritlce = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()
    like_article = LikeArticle.Field()
    create_comment = CreateComment.Field()
    update_comment = UpdateCommet.Field()
    delete_comment = DeleteComment.Field()