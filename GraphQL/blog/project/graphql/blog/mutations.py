from typing import Any

from graphene import Field, ObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from ...blog import models
from .types import (
    ArticleNode,
    ArticleCreateInputType,
    ArticleDeleteInputType,
    ArticleUpdateInputType,
    FavoriteInputType,
    CommentNode,
    CommentCreateInputType,
    CommentDeleteInputType,
    CommentUpdateInputType,
)
from ...core.mutations import AppResolverInfo, BaseMutation



class CreateArticleMutation(BaseMutation):
    article = Field(ArticleNode)
    
    Input = ArticleCreateInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, **data: Any):
        article = models.Article(**data, author=info.context.user)
        article.save()
        return CreateArticleMutation(success=True, article=article)


class DeleteArticleMutation(BaseMutation):
    Input = ArticleDeleteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, **data: Any):
        article = models.Article.objects.select_related("author").get(slug=data.get("slug"))
        if article.author != info.context.user:
            raise GraphQLError("권한 없음")
        article.delete()
        return DeleteArticleMutation(success=True)


class UpdateArticleMutation(BaseMutation):
    Input = ArticleUpdateInputType
    
    article =Field(ArticleNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, **data: Any):
        article = models.Article.objects.select_related("author").get(slug=data.pop("slug"))
        if article.author != info.context.user:
            raise GraphQLError("권한 없음")
        # article.title = data["title"]
        # article.description = data["description"]
        # article.body = data["body"]
        for key, value in data.items():
            setattr(article, key, value)
        article.save()
        return UpdateArticleMutation(success=True, article=article)


class FavoriteArticleMutation(BaseMutation):
    Input = FavoriteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, article_slug) -> "FavoriteArticleMutation":
        article = models.Article.objects.get(slug=article_slug)
        favorite = models.FavoriteArticles.objects.filter(user=info.context.user, article=article)
        if favorite:
            favorite.delete()
        else:
            favorite = models.FavoriteArticles(user=info.context.user, article=article)
            favorite.save()
        return FavoriteArticleMutation(success=True)


class CreateCommentMutation(BaseMutation):
    comment = Field(CommentNode)

    Input = CommentCreateInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, article_slug, body):
        article = models.Article.objects.get(slug=article_slug)
        comment = models.Comment(body=body, author=info.context.user, article=article)
        comment.save()
        article.comment_set.add(comment)
        return CreateCommentMutation(success=True, comment=comment)


class DeleteCommentMutation(BaseMutation):
    Input = CommentDeleteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, comment_id):
        comment = models.Comment.objects.get(id=comment_id)
        if comment.author != info.context.user:
            raise GraphQLError("권한이 없습니다")
        comment.delete()
        return DeleteCommentMutation(success=True)



class UpdateCommentMutation(BaseMutation):
    comment = Field(CommentNode)
    Input = CommentUpdateInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, comment_id, **data):
        comment = models.Comment.objects.get(id=comment_id)
        if comment.author != info.context.user:
            raise GraphQLError("권한이 없습니다")
        for key, value in data.items():
            setattr(comment, key, value)
        comment.save()
        return UpdateCommentMutation(success=True)



