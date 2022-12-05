from ...article import models
from graphene_django import DjangoObjectType
from graphene import relay

class ArticleType(DjangoObjectType):
    class Meta:
        model = models.Article
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = models.Comment
        fields = "__all__"


class LikeType(DjangoObjectType):
    class Meta:
        model = models.Like
        fields = "__all__"