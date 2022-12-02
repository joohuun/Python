from article.models import Article, Comment, Like
from graphene_django import DjangoObjectType

class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = "__all__"
