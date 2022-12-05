import graphene
from ...models import models
from ...article import models
from graphql import GraphQLError
from project.graphql.article.types import ArticleType, CommentType, LikeType
from graphql_jwt.decorators import login_required


class CreateArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()

    article = graphene.Field(ArticleType)

    @classmethod
    @login_required
    def mutate(cls, root, info, title, body):
        if info.context.user:
            print(info.context.user.id)
        article = models.Article(title=title, body=body)
        user = models.User.objects.get(id=info.context.user.id)
        is_verified = user.status.verified
        if not is_verified:
            raise GraphQLError("인증되지 않은 사용자입니다")

        article.user = user
        article.save()
        return CreateArticle(article=article)


class UpdateArticle(graphene.Mutation):
    class Arguments:
        art_id = graphene.ID()
        title = graphene.String()
        body = graphene.String()

    article = graphene.Field(ArticleType)

    @classmethod
    @login_required
    def mutate(cls , root, info, art_id, title, body):
        article = models.Article.objects.get(id=art_id)
        user = info.context.user
        if article.user.id != user.id:
            raise GraphQLError("인증되지 않은 사용자입니다")
        article.title = title
        article.body = body
        article.save()
        return UpdateArticle(article=article)


class DeleteArticle(graphene.Mutation):
    class Arguments:
        art_id = graphene.ID()

    article = graphene.Field(ArticleType)
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, art_id):
        article = models.Article.objects.get(id=art_id)
        user = info.context.user
        if article.user.id != user.id:
            raise GraphQLError("인증되지 않은 사용자입니다")
        article.delete()
        return DeleteArticle(success=True, article=article)


class LikeArticle(graphene.Mutation):
    class Arguments:
        art_id = graphene.ID()

    article = graphene.Field(ArticleType)
    
    @classmethod
    @login_required
    def mutate(cls, root, info, art_id):
        user = models.User.objects.get(id=info.context.user.id)        
        article = models.Article.objects.get(id=art_id)
        like = models.Like.objects.filter(user=user, article=article)

        if like:
            like.delete()
            return
        like = models.Like(article=article, user=user)
        like.save()
        return LikeArticle(article=article)
        

class CreateComment(graphene.Mutation):

    class Arguments:
        art_id = graphene.ID()
        comment = graphene.String()

    article = graphene.Field(CommentType)
    success = graphene.Boolean()


    @classmethod
    @login_required
    def mutate(cls, root, info, art_id, comment):
        user = models.User.objects.get(id=info.context.user.id)
        article = models.Article.objects.get(id=art_id)
        comment = models.Comment(body=comment, user=user, article=article)
        comment.save()
        return CreateComment(success=True, article=comment)


class UpdateCommet(graphene.Mutation):
    class Arguments:
        comment_id = graphene.Int()
        body = graphene.String()

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, comment_id, body):
        user = models.User.objects.get(id=info.context.user.id)
        print(user.id)
        
        comment = models.Comment.objects.get(id=comment_id)
        if comment.user.id != user.id:
            raise GraphQLError("인증되지 않은 사용자입니다")
        comment.body = body
        comment.save()
        return UpdateCommet(success=True, comment=comment)
        



class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.Int()

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, comment_id):
        user = models.User.objects.get(id=info.context.user.id)
        comment = models.Comment.objects.get(id=comment_id)
        print(comment.body)
        if comment.user.id != user.id:
            raise GraphQLError("인증되지 않은 사용자입니다")
        # comment.body = body
        comment.delete()
        return DeleteComment(success=True, comment=comment)