from ...article import models
from graphene_django import DjangoObjectType
from graphene import Field

class ArticleType(DjangoObjectType):
    class Meta:
        model = models.Article
        fields = "__all__"


class LikeType(DjangoObjectType):
    class Meta:
        model = models.Like
        fields = "__all__"
        # fields = ("user")


class CommentType(DjangoObjectType):
    class Meta:
        model = models.Comment
        fields = "__all__"





